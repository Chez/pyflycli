import typer

from rich.console import Console
from rich.table import Table


console = Console()


class TablePrinter:
    def print_response(self, all_responses):
        console.print("\n[bold green]Responses[/bold green]!", "✈")
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("id #", style="dim", width=6)
        table.add_column("Time Aquired", min_width=20)
        table.add_column("Most Recent", min_width=12, justify="right")
    
        limit = 10
        for response in all_responses[::-1][:limit]:
            c = "green" if response.id == all_responses[-1].id else "white"
            is_most_recent = '✅' if response.id == all_responses[-1].id else '❌'
            table.add_row(str(response.id), f'[{c}]{response.time_created}[/{c}]', is_most_recent) 
        
        console.print(table)
        
        
    def print_detailed(self, all_flights):
        console.print("\n[bold green]DetailedFlights[/bold green]!", "✈")
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("id", style="dim", width=6)
        table.add_column("response_id", width=12)
        table.add_column("identification", min_width=6)
        table.add_column("airline_name", min_width=20)
        table.add_column("airplane_code", min_width=6, justify="right")

        limit = 10
        for flight in all_flights[::-1][:limit]:
            c = "white"
            table.add_row(f'[{c}]{flight.id}[/{c}]', f'[green]{flight.response_id}[/green]', f'[{c}]{flight.identification}[/{c}]', f'[{c}]{flight.airline_name}[/{c}]',  f'[{c}]{flight.airplane_code}[/{c}]') 
            
        console.print(table)
        
    def print_brief(self, all_flights):
        console.print("\n[bold green]BriefFlights[/bold green]!", "✈")
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("id", style="dim", width=6)
        table.add_column("identification", width=10)
        table.add_column("response_id", width=12)
        table.add_column("registration", min_width=6)
        table.add_column("lat", min_width=6)
        table.add_column("lon", min_width=6)
        table.add_column("origin", min_width=10)
        table.add_column("destination", min_width=10)
        table.add_column("speed", min_width=10)
        table.add_column("vertical speed", min_width=6, justify="right")

        limit = 10
        for flight in all_flights[::-1][:limit]:
            c = "white"
            table.add_row(f'[{c}]{flight.id}[/{c}]', f'[{c}]{flight.flight_id}[/{c}]', f'[green]{flight.response_id}[/green]', f'[{c}]{flight.registration}[/{c}]', f'[{c}]{flight.lat}[/{c}]', f'[{c}]{flight.lon}[/{c}]',  f'[{c}]{flight.origin}[/{c}]',f'[{c}]{flight.destination}[/{c}]', f'[{c}]{flight.speed}[/{c}]',  f'[{c}]{flight.vertical_speed}[/{c}]') 
            
        console.print(table)