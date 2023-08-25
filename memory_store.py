from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board
    from board_list import BoardList

from data_store import DataStore


class InMemoryStore(DataStore):
    def __init__(self):
        self.boards: dict[int, "Board"] = {}
        self.board_lists: dict[int, list["BoardList"]] = {}

    def add_board(self, board: "Board"):
        self.boards[board.board_id] = board

    def get_board(self, board_id: int):
        return self.boards[board_id]

    def update_board(self, board: "Board", update: dict):
        for k in update:
            setattr(board, k, update[k])

    def get_boards(self):
        return [self.boards[b] for b in self.boards]

    def remove_board(self, board: "Board"):
        del self.boards[board.board_id]
        self.board_lists[board.board_id] = []

    def add_list(self, board: int, launch: "BoardList"):
        if board in self.board_lists:
            self.board_lists[board].append(launch)
        else:
            self.board_lists[board] = [launch]

    def get_lists_by_board(self, board: int):
        return self.board_lists.get(board, [])

    def remove_list(self, board: int, launch_id: int):
        self.board_lists[board] = [
            item for item in self.board_lists[board] if not item.board_list_id == launch_id]
