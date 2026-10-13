from worlds.Files import APTokenTypes

from . import FE8TestBase
from ..connector_config import (
    LEVEL_CAPS_OFFS,
    WEAPON_LEVEL_CAPS_OFFS,
    PROMOTION_UNLOCKS_OFFS,
    RECRUIT_CHECKS_OFFS,
)
from ..rom import FE8ProcedurePatch, write_tokens


def _written_bytes(world) -> dict[int, bytes]:
    """Runs `write_tokens` and returns {offset: bytes} for every WRITE token."""
    patch = FE8ProcedurePatch(
        player=world.player, player_name=world.multiworld.player_name[world.player]
    )
    write_tokens(world, patch)
    return {
        offs: data
        for token_type, offs, data in patch._tokens
        if token_type == APTokenTypes.WRITE
    }


class TestRomOptionsRecruitChecksOn(FE8TestBase):
    options = {"recruit_checks_enabled": True}

    def test_rom_flags(self) -> None:
        written = _written_bytes(self.world)
        self.assertEqual(written[RECRUIT_CHECKS_OFFS], b"\x01")
        self.assertEqual(written[LEVEL_CAPS_OFFS], b"\x01")
        self.assertEqual(written[WEAPON_LEVEL_CAPS_OFFS], b"\x01")
        self.assertEqual(written[PROMOTION_UNLOCKS_OFFS], b"\x00")


class TestRomOptionsRecruitChecksOff(FE8TestBase):
    options = {"recruit_checks_enabled": False}

    def test_rom_flags(self) -> None:
        # The flag must be written explicitly, even though 0 is the ROM default.
        written = _written_bytes(self.world)
        self.assertEqual(written[RECRUIT_CHECKS_OFFS], b"\x00")
        self.assertEqual(written[LEVEL_CAPS_OFFS], b"\x01")
        self.assertEqual(written[WEAPON_LEVEL_CAPS_OFFS], b"\x01")
