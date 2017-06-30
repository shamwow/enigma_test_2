from datetime import datetime

def _insert(char, perms):
    output = []
    for perm in perms:
        for idx, c in enumerate(perm):
            output.append(perm[:idx] + [char] + perm[idx:])

        output.append(perm + [char])

    return output


def _compute_permutations(chars):
    if (len(chars) == 1):
        return [chars]

    return _insert(chars[0], _compute_permutations(chars[1:]))

def _map_join(char, array):
    return map(lambda e: char.join(e), array)

simple_date_formats = []
simple_date_formats += _map_join('-', _compute_permutations(['%Y', '%d', '%m']))
simple_date_formats += _map_join('-', _compute_permutations(['%Y', '%d', '%M']))
simple_date_formats += _map_join('-', _compute_permutations(['%y', '%d', '%m']))
simple_date_formats += _map_join('-', _compute_permutations(['%y', '%d', '%M']))
simple_date_formats += _map_join('/', _compute_permutations(['%Y', '%d', '%m']))
simple_date_formats += _map_join('/', _compute_permutations(['%Y', '%d', '%M']))
simple_date_formats += _map_join('/', _compute_permutations(['%y', '%d', '%m']))
simple_date_formats += _map_join('/', _compute_permutations(['%y', '%d', '%M']))
simple_date_formats += _map_join('-', _compute_permutations(['%Y', '%d', '%b']))
simple_date_formats += _map_join('-', _compute_permutations(['%Y', '%d', '%B']))
simple_date_formats += _map_join('-', _compute_permutations(['%y', '%d', '%b']))
simple_date_formats += _map_join('-', _compute_permutations(['%y', '%d', '%B']))
simple_date_formats += _map_join(' ', _compute_permutations(['%Y', '%d', '%b']))
simple_date_formats += _map_join(' ', _compute_permutations(['%Y', '%d', '%B']))
simple_date_formats += _map_join(' ', _compute_permutations(['%y', '%d', '%b']))
simple_date_formats += _map_join(' ', _compute_permutations(['%y', '%d', '%B']))

replace_day = lambda date: date.replace(day=1)
replace_year = lambda date: date.replace(year=datetime.now().year)
replace_nothing = lambda date: date

date_formats = {
    '%Y-%m': replace_day,
    '%m-%Y': replace_day,
    '%m/%Y': replace_day,

    '%Y-%b': replace_day,
    '%b-%Y': replace_day,
    '%b %Y': replace_day,

    '%Y-%B': replace_day,
    '%B-%Y': replace_day,
    '%B %Y': replace_day,

    '%m/%d': replace_year,
    '%d/%m': replace_year,
    '%M/%d': replace_year,
    '%d/%M': replace_year,

    '%m %d': replace_year,
    '%d %m': replace_year,
    '%M %d': replace_year,
    '%d %M': replace_year,

    '%m-%d': replace_year,
    '%d-%m': replace_year,
    '%M-%d': replace_year,
    '%d-%M': replace_year,
}

for simple_date_format in simple_date_formats:
    date_formats[simple_date_format] = replace_nothing

