import typer


(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "to-do id error",
}

class Log:
    def good(self):
        message = "[INFO] Database status: "
        status = typer.style("good", fg=typer.colors.GREEN, bold=True)
        
    def bad(self):
        message = "[INFO] Database status: "
        status = typer.style("bad", fg=typer.colors.GREEN, bold=True)
        
    def success_local_db(self):
        message = "[INFO] Database status: "
        status = typer.style("no postgres. loaded local sqlite db", fg=typer.colors.GREEN, bold=True)
        typer.echo(message + status)

    def postgres_fail(self):
        message = "[INFO] Database status: "
        status = typer.style("postgres db failed.", fg=typer.colors.RED, bold=True)
        typer.echo(message + status)