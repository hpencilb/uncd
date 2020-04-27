import click
from uncd.UnicodeUtility import *


@click.group()
def cli():
    pass


@cli.command()
@click.option('-c', '--code', default=None)
@click.option('-l', '--letter', default=None)
def f(code, letter):
    """find info about the given Unicode"""
    if not code and not letter:
        click.echo('Please provide --code or --letter', err=True)
    else:
        if code:
            u = UnicodeInfo(code)
        else:
            u = UnicodeInfo(letter=letter)
        if u.flag:
            u.getUnicodeInfo()
            try:
                click.echo(u.code.encode('utf8').decode('unicode_escape'))
            except Exception as e:
                print(e)
            click.echo(f'Name\t\t{u.info["Name"]}')
            click.echo(f'Unicode number\t{u.info["Unicode number"]}')
            click.echo(f'HTML\t\t{u.info["HTML"]}')
            click.echo(f'CSS-code\t{u.info["CSS-code"]}')
            if u.info["Entity"]:
                click.echo(f'Entity\t\t{u.info["Entity"]}')
            click.echo(f'Block\t\t{u.info["Block"]}')
            if u.info["Unicode version"]:
                click.echo(f'Unicode version\t{u.info["Unicode version"]}')
        else:
            click.echo('Unicode Format Error, only accept \'0000\'-\'FFFFF\'', err=True)


@cli.command()
@click.argument('block_name', nargs=-1)
def b(block_name):
    """find all the Unicode in the block"""
    name = ' '.join(block_name)
    u = UnicodeBlock(name)
    if u.flag:
        begin = int(u.begin, 16)
        end = int(u.end, 16)
        li = []
        for i in range(begin, end + 1):
            li.append(fillCode(i))
        count = 0
        for item in li:
            count += 1
            click.echo(item.encode('utf8').decode('unicode_escape') + ' ', nl=False)
            if count % 16 == 0:
                click.echo()
                count = 0
    else:
        click.echo('Block not exists!', err=True)

# if __name__ == '__main__':
#     cli()
