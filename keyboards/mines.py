# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from aiogram.filters.callback_data import CallbackData
# from database import requests as rq


# class mines_moves(CallbackData, prefix = "mines"):
#     bombs: str
#     moves: str
#     play: str


# async def mines():
#     keyboard = InlineKeyboardBuilder()
#     for i in range(1, 25):
#         keyboard.add(InlineKeyboardButton(text = f'{i}', callback_data = f"mines_{i}"))
#     return keyboard.adjust(8).as_markup()

# async def play_mines(bombs: str, moves: str, play : str = "yes") -> InlineKeyboardMarkup:
#     move_in_bombs = False
#     keyboard = InlineKeyboardBuilder()
#     bombs_list = list(map(int, bombs.split("_")[:-1]))
#     moves_list = list(map(int, moves.split("_")[:-1]))

#     if play == "yes":
#         for move in moves_list:
#             if move in bombs_list:
#                 move_in_bombs = True
#                 break

#         if move_in_bombs == False:
#             for i in range(1, 26):
#                 print(i, moves_list)
#                 if i in bombs_list:
#                     keyboard.add(InlineKeyboardButton(text = f'ㅤ', callback_data = mines_moves(bombs = bombs, moves = moves + f'{i}_', play = "no").pack()))
#                 elif i in moves_list:
#                     keyboard.add(InlineKeyboardButton(text = f'💎', callback_data = f"ignore"))
#                 else:
#                     keyboard.add(InlineKeyboardButton(text = f'ㅤ', callback_data = mines_moves(bombs = bombs, moves = moves + f'{i}_', play = "yes").pack()))
#         else:
#             for i in range(1, 26):
#                 if i in bombs_list:
#                     keyboard.add(InlineKeyboardButton(text = f'💣', callback_data = f"ignore"))
#                 else:
#                     keyboard.add(InlineKeyboardButton(text = f'💎', callback_data = f"ignore"))
#             keyboard.add(InlineKeyboardButton(text = f'Вы проиграли!', callback_data = f"loose"))
            
#     elif play == "no":
#         for i in range(1, 26):
#             if i in bombs_list:
#                 keyboard.add(InlineKeyboardButton(text = f'💣', callback_data = "ignore"))
#             else:
#                 keyboard.add(InlineKeyboardButton(text = f'💎', callback_data = "ignore"))
    
#     return keyboard.adjust(5).as_markup()