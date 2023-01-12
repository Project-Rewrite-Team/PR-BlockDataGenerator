import os

from .logger import log
import json
from os import path, makedirs


def get_path(directory: str, namespace: str, template: str, name: str=None):
    _tmp = {
        "bs":path.join(directory,"assets",namespace,"blockstates"),
        "bm":path.join(directory,"assets",namespace,"models","block"),
        "im":path.join(directory,"assets",namespace,"models","item"),
        "ltb":path.join(directory,"data",namespace,"loot_tables","blocks")
    }[template]

    return path.join(_tmp, name+".json") if name else _tmp


def patch_name(namespace: str, name: str, add_tag: str=None, remove_namespace: bool=False):
    if remove_namespace and ":" in name:
        return name[name.index(":")+1:]
    elif remove_namespace:
        return name
    if add_tag and ":" in name:
        _tmp = name.split(":")
        _tmp[1] = add_tag+_tmp[1]
        return ":".join(_tmp)
    elif add_tag:
        return f"{namespace}:{add_tag}{name}"
    return name if ":" in name else f"{namespace}:{name}"


class Template:
    class BlockStates:
        @staticmethod
        def default(namespace: str, name: str):
            _name = patch_name(namespace, name, add_tag="block/")
            return {
                "variants": {
                    "": {
                        "model": _name
                    }
                }
            }

        @staticmethod
        def pillared_block(namespace: str, name: str, name_horizontal: str=None):
            _name = patch_name(namespace, name, add_tag="block/")
            _name_horizontal = patch_name(namespace, name_horizontal, add_tag="block/") or _name+"_horizontal"
            return {
                "variants": {
                    "axis=x": {
                        "model": _name_horizontal,
                        "x": 90,
                        "y": 90
                    },
                    "axis=y": {
                        "model": _name
                    },
                    "axis=z": {
                        "model": _name_horizontal,
                        "x": 90
                    }
                }
            }

    class Models:
        class Block:
            @staticmethod
            def default(namespace: str, name: str):
                _name = patch_name(namespace, name, add_tag="block/")
                return {
                    "parent": "minecraft:block/cube_all",
                    "textures": {
                        "all": _name
                    }
                }

            @staticmethod
            def leaves(namespace: str, name: str):
                _name = patch_name(namespace, name, add_tag="block/")
                return {
                    "parent": "minecraft:block/leaves",
                    "textures": {
                        "all": _name
                    }
                }

            @staticmethod
            def pillared_block(namespace: str, name: str, name_end=None):
                _name = patch_name(namespace, name, add_tag="block/")
                _name_end = patch_name(namespace, name_end, add_tag="block/") if name_end else _name + "_end"
                _tmp1 = {
                    "parent": "minecraft:block/cube_column",
                    "textures": {
                        "end": _name_end,
                        "side": _name
                    }
                }
                _tmp2 = _tmp1.copy()
                _tmp2.update({"parent":"minecraft:block/cube_column_horizontal"})
                log(_tmp2)
                return _tmp1, _tmp2

            @staticmethod
            def sapling(namespace: str, name: str):
                _name = patch_name(namespace, name, add_tag="block/")
                return {
                    "parent": "minecraft:block/cross",
                    "textures": {
                        "cross": _name
                    }
                }

            @staticmethod
            def sign(namespace: str, name_particles: str):
                _name_particles = patch_name(namespace, name_particles, add_tag="block/")
                return {
                    "textures": {
                        "particle": _name_particles
                    }
                }

        class Item:
            @staticmethod
            def item(namespace: str, name: str):
                _name = patch_name(namespace, name, add_tag="item/")
                return {
                    "parent": "item/generated",
                    "textures": {
                        "layer0": _name
                    }
                }

            @staticmethod
            def block(namespace: str, name: str):
                _name = patch_name(namespace, name, add_tag="item/")
                return {
                    "parent": _name
                }

    class LootTable:
        class Blocks:
            @staticmethod
            def custom_ore(namespace: str, name: str, name_ore: str, max_dropped: int, min_dropped: int):
                _name = patch_name(namespace, name)
                _name_ore = patch_name(namespace, name_ore)
                return {
                    "type": "minecraft:block",
                    "pools": [
                        {
                            "bonus_rolls": 0.0,
                            "entries": [
                                {
                                    "type": "minecraft:item",
                                    "conditions": [
                                        {
                                            "condition": "minecraft:match_tool",
                                            "predicate": {
                                                "enchantments": [
                                                    {
                                                        "enchantment": "minecraft:silk_touch",
                                                        "levels": {
                                                            "min": 1
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ],
                                    "name": _name
                                },
                                {
                                    "type": "minecraft:item",
                                    "functions": [
                                        {
                                            "add": False,
                                            "count": {
                                                "type": "minecraft:uniform",
                                                "max": max_dropped,
                                                "min": min_dropped
                                            },
                                            "function": "minecraft:set_count"
                                        },
                                        {
                                            "enchantment": "minecraft:fortune",
                                            "formula": "minecraft:uniform_bonus_count",
                                            "function": "minecraft:apply_bonus",
                                            "parameters": {
                                                "bonusMultiplier": 1
                                            }
                                        },
                                        {
                                            "function": "minecraft:explosion_decay"
                                        }
                                    ],
                                    "name": _name_ore
                                }
                            ],
                            "rolls": 1.0
                        }
                    ]
                }

            @staticmethod
            def ore(namespace: str, name: str, name_ore: str):
                _name = patch_name(namespace, name)
                _name_ore = patch_name(namespace, name_ore)
                return {
                    "type": "minecraft:block",
                    "pools": [
                        {
                            "bonus_rolls": 0.0,
                            "entries": [
                                {
                                    "type": "minecraft:alternatives",
                                    "children": [
                                        {
                                            "type": "minecraft:item",
                                            "conditions": [
                                                {
                                                    "condition": "minecraft:match_tool",
                                                    "predicate": {
                                                        "enchantments": [
                                                            {
                                                                "enchantment": "minecraft:silk_touch",
                                                                "levels": {
                                                                    "min": 1
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ],
                                            "name": _name
                                        },
                                        {
                                            "type": "minecraft:item",
                                            "functions": [
                                                {
                                                    "enchantment": "minecraft:fortune",
                                                    "formula": "minecraft:ore_drops",
                                                    "function": "minecraft:apply_bonus"
                                                },
                                                {
                                                    "function": "minecraft:explosion_decay"
                                                }
                                            ],
                                            "name": _name_ore
                                        }
                                    ]
                                }
                            ],
                            "rolls": 1.0
                        }
                    ]
                }

            @staticmethod
            def drops_self(namespace: str, name: str):
                _name = patch_name(namespace, name)
                return {
                    "type": "minecraft:block",
                    "pools": [
                        {
                            "bonus_rolls": 0.0,
                            "conditions": [
                                {
                                    "condition": "minecraft:survives_explosion"
                                }
                            ],
                            "entries": [
                                {
                                    "type": "minecraft:item",
                                    "name": _name
                                }
                            ],
                            "rolls": 1.0
                        }
                    ]
                }

            @staticmethod
            def stone_like(namespace: str, name: str, name_dropped: str):
                _name = patch_name(namespace, name)
                _name_dropped = patch_name(namespace, name_dropped)
                return {
                    "type": "minecraft:block",
                    "pools": [
                        {
                            "bonus_rolls": 0.0,
                            "entries": [
                                {
                                    "type": "minecraft:alternatives",
                                    "children": [
                                        {
                                            "type": "minecraft:item",
                                            "conditions": [
                                                {
                                                    "condition": "minecraft:match_tool",
                                                    "predicate": {
                                                        "enchantments": [
                                                            {
                                                                "enchantment": "minecraft:silk_touch",
                                                                "levels": {
                                                                    "min": 1
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            ],
                                            "name": _name
                                        },
                                        {
                                            "type": "minecraft:item",
                                            "conditions": [
                                                {
                                                    "condition": "minecraft:survives_explosion"
                                                }
                                            ],
                                            "name": _name_dropped
                                        }
                                    ]
                                }
                            ],
                            "rolls": 1.0
                        }
                    ]
                }

            @staticmethod
            def leaves(namespace: str, name: str, name_sapling: str, name_stick: str="minecraft:stick"):
                _name = patch_name(namespace, name)
                _name_sapling = patch_name(namespace, name_sapling)
                _name_stick = patch_name(namespace, name_stick)
                return {
                    "type": "minecraft:block",
                    "pools": [
                        {
                            "bonus_rolls": 0.0,
                            "entries": [
                                {
                                    "type": "minecraft:alternatives",
                                    "children": [
                                        {
                                            "type": "minecraft:item",
                                            "conditions": [
                                                {
                                                    "condition": "minecraft:alternative",
                                                    "terms": [
                                                        {
                                                            "condition": "minecraft:match_tool",
                                                            "predicate": {
                                                                "items": [
                                                                    "minecraft:shears"
                                                                ]
                                                            }
                                                        },
                                                        {
                                                            "condition": "minecraft:match_tool",
                                                            "predicate": {
                                                                "enchantments": [
                                                                    {
                                                                        "enchantment": "minecraft:silk_touch",
                                                                        "levels": {
                                                                            "min": 1
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    ]
                                                }
                                            ],
                                            "name": _name
                                        },
                                        {
                                            "type": "minecraft:item",
                                            "conditions": [
                                                {
                                                    "condition": "minecraft:survives_explosion"
                                                },
                                                {
                                                    "chances": [
                                                        0.05,
                                                        0.0625,
                                                        0.083333336,
                                                        0.1
                                                    ],
                                                    "condition": "minecraft:table_bonus",
                                                    "enchantment": "minecraft:fortune"
                                                }
                                            ],
                                            "name": _name_sapling
                                        }
                                    ]
                                }
                            ],
                            "rolls": 1.0
                        },
                        {
                            "bonus_rolls": 0.0,
                            "conditions": [
                                {
                                    "condition": "minecraft:inverted",
                                    "term": {
                                        "condition": "minecraft:alternative",
                                        "terms": [
                                            {
                                                "condition": "minecraft:match_tool",
                                                "predicate": {
                                                    "items": [
                                                        "minecraft:shears"
                                                    ]
                                                }
                                            },
                                            {
                                                "condition": "minecraft:match_tool",
                                                "predicate": {
                                                    "enchantments": [
                                                        {
                                                            "enchantment": "minecraft:silk_touch",
                                                            "levels": {
                                                                "min": 1
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "entries": [
                                {
                                    "type": "minecraft:item",
                                    "conditions": [
                                        {
                                            "chances": [
                                                0.02,
                                                0.022222223,
                                                0.025,
                                                0.033333335,
                                                0.1
                                            ],
                                            "condition": "minecraft:table_bonus",
                                            "enchantment": "minecraft:fortune",
                                        }
                                    ],
                                    "functions": [
                                        {
                                            "add": False,
                                            "count": {
                                                "type": "minecraft:uniform",
                                                "max": 2.0,
                                                "min": 1.0
                                            },
                                            "function": "minecraft:set_count"
                                        },
                                        {
                                            "function": "minecraft:explosion_decay"
                                        }
                                    ],
                                    "name": _name_stick
                                }
                            ],
                            "rolls": 1.0
                        }
                    ]
                }


class BlockTools:
    @staticmethod
    def make_file(directory: str, namespace: str, name: str, template: str, data: dict):
        makedirs(get_path(directory, namespace, template), exist_ok=True)
        with open(get_path(directory, namespace, template, name), "w+") as file:
            json.dump(data, file, indent=4)

    class NewBlock:
        @staticmethod
        def generic(directory: str, namespace: str, name: str, name_dropped: str=None):
            print(directory)
            log("[{}] Generating Json data...", mixins=[name])
            _blockstate = Template.BlockStates.default(namespace, name)
            _block_model = Template.Models.Block.default(namespace, name)
            _item_model = Template.Models.Item.block(namespace, name)
            _loot_table = Template.LootTable.Blocks.drops_self(namespace, name) if not name_dropped else Template.LootTable.Blocks.stone_like(namespace, name, name_dropped)
            log("[{}] Writing Json data to files...", mixins=[name])
            BlockTools.make_file(directory, namespace, name, "bs", _blockstate)
            BlockTools.make_file(directory, namespace, name, "bm", _block_model)
            BlockTools.make_file(directory, namespace, name, "im", _item_model)
            BlockTools.make_file(directory, namespace, name, "ltb", _loot_table)
            log("[{}] All tasks completed.", mixins=[name])

        @staticmethod
        def pillar(directory: str, namespace: str, name: str, name_dropped: str=None, name_end: str=None):
            log("[{}] Generating Json data...", mixins=[name])
            _blockstate = Template.BlockStates.pillared_block(namespace, name)
            _block_model, _block_model_horizontal = Template.Models.Block.pillared_block(namespace, name, name_end)
            _item_model = Template.Models.Item.block(namespace, name)
            _loot_table = Template.LootTable.Blocks.drops_self(namespace, name) if not name_dropped else Template.LootTable.Blocks.stone_like(namespace, name, name_dropped)
            log("[{}] Writing Json data to files...", mixins=[name])
            BlockTools.make_file(directory, namespace, name, "bs", _blockstate)
            BlockTools.make_file(directory, namespace, name, "bm", _block_model)
            BlockTools.make_file(directory, namespace, name+"_horizontal", "bm", _block_model_horizontal)
            BlockTools.make_file(directory, namespace, name, "im", _item_model)
            BlockTools.make_file(directory, namespace, name, "ltb", _loot_table)
            log("[{}] All tasks completed.", mixins=[name])

        @staticmethod
        def ore(directory: str, namespace: str, name: str, name_dropped: str=None, dropped: tuple or list=None):
            log("[{}] Generating Json data...", mixins=[name])
            _blockstate = Template.BlockStates.default(namespace, name)
            _block_model = Template.Models.Block.default(namespace, name)
            _item_model = Template.Models.Item.block(namespace, name)
            _loot_table = Template.LootTable.Blocks.ore(namespace, name, name_dropped) if not dropped else Template.LootTable.Blocks.custom_ore(namespace, name, name_dropped, dropped[0], dropped[1])
            log("[{}] Writing Json data to files...", mixins=[name])
            BlockTools.make_file(directory, namespace, name, "bs", _blockstate)
            BlockTools.make_file(directory, namespace, name, "bm", _block_model)
            BlockTools.make_file(directory, namespace, name, "im", _item_model)
            BlockTools.make_file(directory, namespace, name, "ltb", _loot_table)
            log("[{}] All tasks completed.", mixins=[name])
