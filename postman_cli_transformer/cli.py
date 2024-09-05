import click


@click.group()
@click.version_option()
def cli():
    "This package will output the STDOUT from Postman CLI collection run and transform the output text to a JSON doc which may in turn be transformed."


@cli.command(name="command")
@click.argument(
    "example"
)
@click.option(
    "-o",
    "--option",
    help="An example option",
)
def first_command(example, option):
    "Command description goes here"
    click.echo("Here is some output")
