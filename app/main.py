"""Main entrypoint."""

from stats import gen_stats
from comparators import compare, compare_pct, print_lowest_and_highest_ce, print_scatter, print_scatter_2, print_scatter_3, print_scatter_4
from rankings import print_rankings

gen_stats()
compare('Ministerio de Defensa')
compare_pct('Ministerio de Defensa')
print_lowest_and_highest_ce()
print_rankings()
print_scatter()
print_scatter_2()
print_scatter_3()
print_scatter_4()
