"""Main entrypoint."""

from stats import gen_stats
from comparators import compare, compare_pct, print_lowest_and_highest_ce
from rankings import print_rankings

gen_stats()
compare('Ministerio de Defensa')
compare_pct('Ministerio de Defensa')
print_lowest_and_highest_ce()
print_rankings()