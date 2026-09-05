from dataclasses import dataclass
import json

# ---------------------------------------------------------------

@dataclass
class Backgrounds:
    menu_background: str
    other_background: str


@dataclass
class Buttons:
    achievements: str
    apply: str
    clue: str
    exit: str
    leaderboard: str
    authors: str
    play_button: str
    restart: str
    settings: str
    update_table: str
    flag: str
    flag_on_field: str


@dataclass
class RadioButtons:
    selected_dot: str
    not_selected_dot: str


@dataclass
class GameUtils:
    field: str
    mine: str


@dataclass
class Logo:
    logo: str


@dataclass
class UiFiles:
    menu: str
    achievements: str
    game: str
    leaderboard: str
    authors: str
    settings: str


@dataclass
class OtherFrontend:
    window_size: tuple[int, int]  


@dataclass
class FrontendConfig:
    backgrounds: Backgrounds
    buttons: Buttons
    radio_buttons: RadioButtons
    game_utils: GameUtils
    logo: Logo
    ui_files: UiFiles
    other_frontend: OtherFrontend


# ---------------------------------------------------------------

@dataclass
class Data:
    achievements: str
    authors: str
    storage: str


@dataclass
class Values:
    count_wins_value: int
    count_marked_mines_value: int


@dataclass
class Texts:
    count_wins_text: str
    count_marked_mines_text: str
    complete_beginner_level_text: str
    complete_professional_level_text: str


@dataclass
class Achievements:
    values: Values
    texts: Texts


@dataclass
class FieldSizes:
    beginner: tuple[int, int]  
    professional: tuple[int, int]


@dataclass
class BeginnerCellParameters:
    cell_size: tuple[int, int]
    shift: int
    start_position: tuple[int, int]  


@dataclass
class ProfessionalCellParameters:
    cell_size: tuple[int, int]  
    shift: int
    start_position: tuple[int, int] 


@dataclass
class CellParameters:
    beginner_cell_parameters: BeginnerCellParameters
    professional_cell_parameters: ProfessionalCellParameters


@dataclass
class FontSettings:
    font_family: str
    font_size: int 


@dataclass
class GameParameters:
    field_sizes: FieldSizes
    cell_parameters: CellParameters
    font_settings: FontSettings


@dataclass
class BackendConfig:
    data: Data
    achievements: Achievements
    game_parameters: GameParameters


# ---------------------------------------------------------------

@dataclass
class Config:
    frontend: FrontendConfig
    backend: BackendConfig


def load_config(path: str = 'data.json') -> Config:
    with open(path, 'r', encoding='utf8') as f:
        raw = json.load(f)

    front = raw['frontend']
    back = raw['backend']

   
    window_width, window_height = map(int, front['other']['window_size'].split(';'))
    beginner_field_width, beginner_field_height = map(int, back['game_parameters']['field_sizes']['beginner_field_size'].split(';'))
    professional_field_width, professional_field_height = map(int, back['game_parameters']['field_sizes']['professional_field_size'].split(';'))

    return Config(
        frontend=FrontendConfig(
            backgrounds=Backgrounds(
                menu_background=front['backgrounds']['menu_background.png'],
                other_background=front['backgrounds']['other_background.png']
            ),
            buttons=Buttons(
                achievements=front['buttons']['achievements.png'],
                apply=front['buttons']['apply.png'],
                clue=front['buttons']['clue.png'],
                exit=front['buttons']['exit.png'],
                leaderboard=front['buttons']['leaderboard.png'],
                authors=front['buttons']['authors.png'],
                play_button=front['buttons']['play_button.png'],
                restart=front['buttons']['restart.png'],
                settings=front['buttons']['settings.png'],
                update_table=front['buttons']['update_table.png'],
                flag=front['buttons']['flag.png'],
                flag_on_field=front['buttons']['flag_on_field.png']
            ),
            radio_buttons=RadioButtons(
                selected_dot=front['radio_buttons']['selected_dot.png'],
                not_selected_dot=front['radio_buttons']['not_selected_dot.png']
            ),
            game_utils=GameUtils(
                field=front['game_utils']['field.png'],
                mine=front['game_utils']['mine.png']
            ),
            logo=Logo(
                logo=front['logo']['logo.ico']
            ),
            ui_files=UiFiles(
                menu=front['ui_files']['menu.ui'],
                achievements=front['ui_files']['achievements.ui'],
                game=front['ui_files']['game.ui'],
                leaderboard=front['ui_files']['leaderboard.ui'],
                authors=front['ui_files']['authors.ui'],
                settings=front['ui_files']['settings.ui']
            ),
            other_frontend=OtherFrontend(
                window_size=(window_width, window_height)
            )
        ),
        backend=BackendConfig(
            data=Data(
                achievements=back['data']['achievements.csv'],
                authors=back['data']['authors.txt'],
                storage=back['data']['storage.sqlite']
            ),
            achievements=Achievements(
                values=Values(
                    count_wins_value=int(back['achievements']['values']['count_wins_value']),
                    count_marked_mines_value=int(back['achievements']['values']['count_marked_mines_value'])
                ),
                texts=Texts(
                    count_wins_text=back['achievements']['texts']['count_wins_text'],
                    count_marked_mines_text=back['achievements']['texts']['count_marked_mines_text'],
                    complete_beginner_level_text=back['achievements']['texts']['complete_beginner_level_text'],
                    complete_professional_level_text=back['achievements']['texts']['complete_professional_level_text']
                )
            ),
            game_parameters=GameParameters(
                field_sizes=FieldSizes(
                    beginner=(beginner_field_width, beginner_field_height),
                    professional=(professional_field_width, professional_field_height),
                ),
                cell_parameters=CellParameters(
                    beginner_cell_parameters=BeginnerCellParameters(
                        cell_size=(int(back['game_parameters']['cell_parameters']['beginner_cell_parameters']['width']),
                                   int(back['game_parameters']['cell_parameters']['beginner_cell_parameters']['height'])),
                        shift=int(back['game_parameters']['cell_parameters']['beginner_cell_parameters']['shift']),
                        start_position=(int(back['game_parameters']['cell_parameters']['beginner_cell_parameters']['x']),
                                        int(back['game_parameters']['cell_parameters']['beginner_cell_parameters']['y']))
                    ),
                    professional_cell_parameters=ProfessionalCellParameters(
                        cell_size=(int(back['game_parameters']['cell_parameters']['professional_cell_parameters']['width']),
                                   int(back['game_parameters']['cell_parameters']['professional_cell_parameters']['height'])),
                        shift=int(back['game_parameters']['cell_parameters']['professional_cell_parameters']['shift']),
                        start_position=(int(back['game_parameters']['cell_parameters']['professional_cell_parameters']['x']),
                                        int(back['game_parameters']['cell_parameters']['professional_cell_parameters']['y']))
                    )
                ),
                font_settings=FontSettings(
                    font_family=back['game_parameters']['font_settings']['font_family'],
                    font_size=int(back['game_parameters']['font_settings']['font_size'])
                )
            )
        )
    )
