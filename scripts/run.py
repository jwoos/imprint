import yaml
import click
import yamlcore

"""
This assumes that we're running from the repo root
"""

DEFAULT_TAG = 'main'

GITHUB_WORKFLOW_PATH = '.github/workflows/build.yml'
GITHUB_WORKFLOW_FMT = 'zmkfirmware/zmk/.github/workflows/build-user-config.yml@{}'

WEST_PATH = 'config/west.yml'


def yaml_dump(content):
    return yaml.dump(
        content,
        default_flow_style=False,
        Dumper=yamlcore.CCoreDumper
    )


def yaml_load(s):
    return yaml.load(s, Loader=yamlcore.CCoreLoader)


def set_github_workflow(tag, apply=False):
    print('Working on github workflow\n----------')

    with open(GITHUB_WORKFLOW_PATH, 'r+') as f:
        parsed = yaml_load(f.read())
        parsed['jobs']['build']['uses'] = GITHUB_WORKFLOW_FMT.format(tag)

        if apply:
            f.truncate()
            f.seek(0)
            f.write(
                yaml_dump(parsed)
            )
        else:
            print(yaml_dump(parsed))


def set_west(zmk_tag, cyboard_tag, apply=False):
    print('working on west\n----------')

    with open(WEST_PATH, 'r+') as f:
        parsed = yaml_load(f.read())
        for project in parsed['manifest']['projects']:
            match project['name']:
                case 'zmk':
                    project['revision'] = zmk_tag
                case 'zmk-keyboards':
                    project['revision'] = cyboard_tag

        if apply:
            f.truncate()
            f.seek(0)
            f.write(
                yaml_dump(parsed)
            )
        else:
            print(yaml_dump(parsed))


@click.command()
@click.option('--cyboard', default=DEFAULT_TAG, help='Cyboard tag to use')
@click.option('--zmk', default=DEFAULT_TAG,
              help='ZMK tag to use')
@click.option('--apply', is_flag=True)
def main(
    cyboard,
    zmk,
    apply
):
    set_github_workflow(zmk, apply=apply)
    set_west(zmk, cyboard, apply=apply)


if __name__ == '__main__':
    main()
