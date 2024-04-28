from pyrogram.types import InlineKeyboardButton

import config
from AnonXMusic import app




def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
        ],
        [
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_70"], callback_data="exp_helper"),
            InlineKeyboardButton(text=_["F_1"], callback_data="settings_back_helper"),
            InlineKeyboardButton(text=_["F_2"], callback_data="ai_features"),
        ],
        [
            InlineKeyboardButton(text=_["S_B_69"], url=f"https://t.me/EonixCore"),   
        ],
    ]
    return buttons


def exp_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),   
            InlineKeyboardButton(text=_["S_B_69"], url=config.SUPPORT_CHANNEL),
        ],
        [
            InlineKeyboardButton(text=_["S_B_143"], callback_data=f"call_sys"),
        ],
        [ 
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"settingsback_helper"),
        ],
    ]
    return buttons


def feature_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["F_1"], callback_data="settings_back_helper"),
            InlineKeyboardButton(text=_["F_2"], callback_data="ai_features"),
        ],
        [ 
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"settingsback_helper"),
        ],
    ]
    return buttons
