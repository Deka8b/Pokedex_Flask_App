import collections

import pypokedex
import requests
from opposite_types import opposite_types, all_evolutions


def get_pokemon_number(name: str):
    pokemon = pypokedex.get(name=name)
    return pokemon.dex


def get_pokemon_description(number: int):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{number}")
    description = response.json().get("flavor_text_entries")[1]["flavor_text"].replace("\n", " ").replace("", " ")
    return description


def get_pokemon_image(number: int):
    pokemon = pypokedex.get(dex=number)
    image = pokemon.sprites.front["default"]
    return image


def get_attacks_list(number: int):
    pokemon = pypokedex.get(dex=number)
    pkmn_moves = {move.level: move.name.replace("-", " ") for move in pokemon.moves["red-blue"] if move.level}
    sorted_pokemon_dict = collections.OrderedDict(sorted(pkmn_moves.items()))
    sorted_dict = {}
    for k, v in sorted_pokemon_dict.items():
        if v not in sorted_dict.values():
            sorted_dict[k] = v
    return sorted_dict


def get_vulnerability_list(number):
    pokemon = pypokedex.get(dex=number)
    enemies_list = [opposite_types[pkmn_type] for pkmn_type in pokemon.types]
    parsed_enemy_list = [elem for elem in enemies_list if type(elem) != list]
    for elem in enemies_list:
        if type(elem) == list:
            for item in elem:
                parsed_enemy_list.append(item)
    return parsed_enemy_list


def get_pokemon_stats(number):
    pokemon = pypokedex.get(dex=number)
    pokemon_stats = {"Atk": pokemon.base_stats.attack, "Def": pokemon.base_stats.defense,
                     "Speed": pokemon.base_stats.speed, "Hp": pokemon.base_stats.hp}
    return pokemon_stats


def get_pokemon_type(number):
    pokemon = pypokedex.get(dex=number)
    return pokemon.types


def get_height_and_weight(number):
    pokemon = pypokedex.get(dex=number)
    height_and_weight = [round(pokemon.height*0.1,2), round(pokemon.weight*0.1, 2)]
    return height_and_weight


def get_evolutions(number):
    pokemon = pypokedex.get(dex=number).name
    for elem in all_evolutions:
        if pokemon in elem:
            return elem


def get_evolution_pictures(number):
    pokemon = pypokedex.get(dex=number).name
    new_list = []
    for elem in all_evolutions:
        if pokemon in elem:
            pokemons_evolution = elem
            for pkmns in pokemons_evolution:
                new_list.append(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pypokedex.get(name=pkmns).dex}.png")

    return new_list


def main():
    name = input("Name: ")
    pokemon = pypokedex.get(name=name)
    number = pokemon.dex
    images = get_pokemon_image(number)
    attacks = get_attacks_list(number)
    type = get_pokemon_type(number)
    enemies = get_vulnerability_list(number)
    stats = get_pokemon_stats(number)
    h_and_w = get_height_and_weight(number)
    evolution = get_evolutions(number)
    evols = get_evolution_pictures(number)


if __name__ == '__main__':
    main()
