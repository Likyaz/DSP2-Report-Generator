import sys
from datetime import date
from getpass import getpass

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich import box

from app.adapter.get_dsp2_api import get_dsp2_api
from app.domain.service.dsp2_service import Dsp2Service
from app.domain.service.report_service import ReportService
from app.domain.service.account_consistency_validator import AccountConsistencyValidator
from app.adapter.get_report_generator import get_report_generator

console = Console()


def show_welcome():
    console.print("[bold red]DSP2 Report Generator[/bold red]", justify="center")


def get_credentials():
    console.print("[bold cyan]Authentication Required[/bold cyan]")
    username = Prompt.ask("Enter username")
    password = Prompt.ask("Enter password", password=True)
    return username, password


def authenticate_user(max_attempts=3):
    for attempt in range(max_attempts):
        try:
            username, password = get_credentials()
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Authenticating...", total=None)
                dsp2_api = get_dsp2_api()
                dsp2_service = Dsp2Service(dsp2_api, username, password)
                progress.update(task, description="Authentication successful!")
            
            console.print("[bold green]Authentication successful![/bold green]")

            return dsp2_service
            
        except Exception as e:
            remaining_attempts = max_attempts - attempt - 1
            if remaining_attempts > 0:
                console.print(f"[red]Authentication failed: {str(e)}[/red]")
                console.print(f"[yellow]Remaining attempts: {remaining_attempts}[/yellow]")
                console.print()
            else:
                console.print(f"[bold red]Authentication failed after {max_attempts} attempts: {str(e)}[/bold red]")
                console.print("[yellow]Please check your credentials and try again.[/yellow]")
                sys.exit(1)


def display_menu():
    menu_table = Table(title="Report Options", box=box.ROUNDED)
    menu_table.add_column("Option", style="cyan", no_wrap=True)
    menu_table.add_column("Description", style="white")
    
    menu_table.add_row("1", "Generate JSON Report")
    menu_table.add_row("2", "Generate CSV Report")
    menu_table.add_row("3", "Generate Consistency Report")
    menu_table.add_row("4", "Exit")
    
    console.print(menu_table)


def get_account_selection(dsp2_service):
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Loading accounts...", total=None)
            accounts = dsp2_service.get_accounts()
            progress.update(task, description="Accounts loaded!")
        
        if not accounts:
            console.print("[red]No accounts found.[/red]")
            return None

        accounts_table = Table(title="Available Accounts", box=box.ROUNDED)
        accounts_table.add_column("#", style="cyan", no_wrap=True)
        accounts_table.add_column("Name", style="green")
        accounts_table.add_column("IBAN", style="yellow")
        accounts_table.add_column("Type", style="magenta")
        
        for i, account in enumerate(accounts, 1):
            accounts_table.add_row(
                str(i),
                account.name,
                account.iban,
                account.type.value
            )
        
        console.print(accounts_table)
        
        while True:
            try:
                choice = Prompt.ask(f"Select account", choices=[str(i) for i in range(1, len(accounts) + 1)])
                return accounts[int(choice) - 1]
            except ValueError:
                console.print("[red]Please enter a valid number[/red]")
                
    except Exception as e:
        console.print(f"[red]Error getting accounts: {str(e)}[/red]")
        return None


def get_date_range():
    console.print("\n[bold cyan]Date Range Selection[/bold cyan]")
    
    while True:
        try:
            start_date_str = Prompt.ask("Enter start date", default="2024-01-01")
            end_date_str = Prompt.ask("Enter end date", default="2024-12-31")
            
            start_date = date.fromisoformat(start_date_str)
            end_date = date.fromisoformat(end_date_str)
            
            if start_date > end_date:
                console.print("[red]Start date cannot be after end date[/red]")
                continue

            date_info = Table(box=box.SIMPLE)
            date_info.add_column("Period", style="cyan")
            date_info.add_column("Date", style="green")
            date_info.add_row("Start Date", start_date_str)
            date_info.add_row("End Date", end_date_str)
            console.print(date_info)

            if Confirm.ask("Confirm date range?", default=True):
                return start_date, end_date
                
        except ValueError:
            console.print("[red]Invalid date format. Please use YYYY-MM-DD[/red]")


def generate_json_report(dsp2_service, account, start_date, end_date):
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating JSON report...", total=None)
            report_service = ReportService(dsp2_service)
            report_json = report_service.generate_report_json(account.id, start_date, end_date)
            progress.update(task, description="JSON report generated!")
        
        filename = f"report_{account.id}_{start_date}_{end_date}.json"
        with open(filename, 'w') as f:
            f.write(report_json)
        
        success_panel = Panel(
            f"JSON report generated successfully!\n[green]File: {filename}[/green]",
            title="[bold green]Success[/bold green]",
            border_style="green"
        )
        console.print(success_panel)
        return True
        
    except Exception as e:
        error_panel = Panel(
            f"Error generating JSON report:\n[red]{str(e)}[/red]",
            title="[bold red]Error[/bold red]",
            border_style="red"
        )
        console.print(error_panel)
        return False


def generate_csv_report(dsp2_service, account, start_date, end_date):
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating CSV report...", total=None)
            report_service = ReportService(dsp2_service)
            csv_content = report_service.generate_report_csv(account.id, start_date, end_date)
            progress.update(task, description="CSV report generated!")
        
        filename = f"report_{account.id}_{start_date}_{end_date}.csv"
        with open(filename, 'w') as f:
            f.write(csv_content)
        
        success_panel = Panel(
            f"CSV report generated successfully!\n[green]File: {filename}[/green]",
            title="[bold green]Success[/bold green]",
            border_style="green"
        )
        console.print(success_panel)
        return True
        
    except Exception as e:
        error_panel = Panel(
            f"Error generating CSV report:\n[red]{str(e)}[/red]",
            title="[bold red]Error[/bold red]",
            border_style="red"
        )
        console.print(error_panel)
        return False


def generate_consistency_report(dsp2_service):
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing account consistency...", total=None)
            errors = AccountConsistencyValidator.validate(dsp2_service)
            progress.update(task, description="Consistency analysis complete!")
        
        if not errors:
            success_panel = Panel(
                "No consistency errors found!",
                title="[bold green]Consistency Check[/bold green]",
                border_style="green"
            )
            console.print(success_panel)
        else:
            errors_table = Table(title="Consistency Errors Found", box=box.ROUNDED)
            errors_table.add_column("#", style="cyan", no_wrap=True)
            errors_table.add_column("Error", style="red")
            
            for i, error in enumerate(errors, 1):
                errors_table.add_row(str(i), error)
            
            console.print(errors_table)
        
        filename = "consistency_report.txt"
        with open(filename, 'w') as f:
            f.write("Consistency Report\n")
            f.write("=" * 20 + "\n\n")
            if not errors:
                f.write("No consistency errors found!\n")
            else:
                f.write(f"Found {len(errors)} consistency errors:\n\n")
                for error in errors:
                    f.write(f"- {error}\n")
        
        file_panel = Panel(
            f"Consistency report saved: [green]{filename}[/green]",
            title="[bold blue]File Saved[/bold blue]",
            border_style="blue"
        )
        console.print(file_panel)
        return True
        
    except Exception as e:
        error_panel = Panel(
            f"Error generating consistency report:\n[red]{str(e)}[/red]",
            title="[bold red]Error[/bold red]",
            border_style="red"
        )
        console.print(error_panel)
        return False


def main():
    try:
        show_welcome()

        dsp2_service = authenticate_user()
        
        while True:
            display_menu()
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"])
            
            if choice == "1":
                account = get_account_selection(dsp2_service)
                if account:
                    start_date, end_date = get_date_range()
                    generate_json_report(dsp2_service, account, start_date, end_date)
                    
            elif choice == "2":
                account = get_account_selection(dsp2_service)
                if account:
                    start_date, end_date = get_date_range()
                    generate_csv_report(dsp2_service, account, start_date, end_date)
                    
            elif choice == "3":
                generate_consistency_report(dsp2_service)
                
            elif choice == "4":
                break
    
                    
    except KeyboardInterrupt:
        console.print("[yellow]Goodbye![/yellow]")
    except Exception as e:
        error_panel = Panel(
            f"Unexpected error:\n[red]{str(e)}[/red]",
            title="[bold red]Fatal Error[/bold red]",
            border_style="red"
        )
        console.print(error_panel)
        sys.exit(1)


if __name__ == "__main__":
    main() 