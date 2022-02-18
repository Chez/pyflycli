import typer

import time

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
    def db_healthy(self):
        message = "[INFO] Database status: "
        status = typer.style("good", fg=typer.colors.GREEN, bold=True)
        
    def db_unhealthy(self):
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
        
    def app_error(self):
        message = "[INFO] Application status: "
        status = typer.style("bad", fg=typer.colors.GREEN, bold=True)

    def healthy(self):
        self.sim_typer_progress()
        message = "[INFO] Application status: "
        status = typer.style("good", fg=typer.colors.GREEN, bold=True)
        typer.echo(message + status)
        

    def sim_typer_progress(self):
        total = 0
        with typer.progressbar(range(100)) as progress:
            for value in progress:
                # Fake processing time
                time.sleep(0.01)
                total += 1
