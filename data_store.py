from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board
    from board_list import BoardList


class DataStore:

    def add_board(self, model) -> None:
        raise NotImplementedError

    def get_board(self, board_id) -> "Board":
        raise NotImplementedError

    def get_boards(self) -> list["Board"]:
        raise NotImplementedError

    def update_board(self, model, update):
        raise NotImplementedError

    def remove_board(self, board) -> None:
        raise NotImplementedError

    def add_list(self, board, model) -> None:
        raise NotImplementedError

    def get_lists(self) -> list["BoardList"]:
        raise NotImplementedError

    def get_list(self, launch_id) -> "BoardList":
        raise NotImplementedError

    def get_lists_by_board(self, board) -> list["BoardList"]:
        raise NotImplementedError

    def remove_list(self, board, launch_id) -> None:
        raise NotImplementedError
