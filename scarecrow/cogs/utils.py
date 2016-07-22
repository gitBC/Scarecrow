"""
This gather stuff that for the most part should be written elsewhere but is not because ¯\_(ツ)_/¯
"""
import aiohttp
import asyncio
import random
import string


def setup(bot):
    pass


async def fetch_page(url, timeout=None, session=None):
    """Fetches a web page and return its text or json content."""
    # Create a session if none has been given
    if session:
        _session = session
    else:
        _session = aiohttp.ClientSession()

    try:
        resp = await asyncio.wait_for(_session.get(url), timeout)
    except asyncio.TimeoutError:
        data = None
    else:
        if resp.status != 200:
            data = 'Http error {}.'.format(resp.status)
        elif resp.headers['content-type'] == 'application/json':
            data = await resp.json()
        else:
            data = await resp.text()

    # Close the session if we created it especially for this fetch
    if not session:
        _session.close()

    return data


def indented_entry_to_str(entries, indent=0, sep=' '):
    """Pretty formatting."""
    # Get the longest keys' width
    # width = [max([len(t[i]) for t in entries]) for i in range(0, len(entries) - 1)]
    width = max([len(t[0]) for t in entries])

    output = []

    # Set the format for each line
    if indent > 0:
        fmt = '{0:{indent}}{1:{width}}{sep}{2}\n'
    else:
        fmt = '{1:{width}}{sep}{2}\n'

    for name, entry in entries:
        output.append(fmt.format('', name, entry, width=width, indent=indent, sep=sep))

    return ''.join(output)


def random_line(file_name, predicate=None):
    """Reservoir algorithm to randomly draw one line from a file."""
    with open(file_name, 'r', encoding='utf-8') as file:
        file = filter(predicate, file)
        line = next(file)
        for num, aline in enumerate(file):
            if random.randrange(num + 2):
                continue
            line = aline
    return line


# -----------------------
# Agarify stuff

def agar_wrap(inner, parens):
    """Utility function to wrap something in a pair of agar parentheses."""
    inner.insert(0, parens[0])
    inner.append(parens[1])


def letter_or_letterlike():
    """Generate a random letter or letterlike symbol."""
    if random.randint(1, 10) > 2:
        # Letter
        return random.choice(random.choice(AGAR_ALPHABETS))
    else:
        # Letterlike
        return random.choice(AGAR_LETTERLIKE)


def agar_clan():
    """ An agar clan name consists of :
            * a random string of letters and letterlike symbols.
            * optionally a regular symbol at the end.
            * one or two pairs of parentheses surrounding it all.
    """
    # 3-4 letters or letterlikes
    clan = [letter_or_letterlike() for i in range(0, random.randint(3, 4))]

    # Optional symbol
    if random.randint(1, 10) > 5:
        clan.append(random.choice(AGAR_SYMBOLS))

    # Parentheses
    agar_wrap(clan, random.choice(AGAR_PARENS))

    # Sometimes a second pair
    if random.randint(1, 100) > 25:
        agar_wrap(clan, random.choice(AGAR_PARENS))

    return clan


def agar_replace(line):
    """Partially agarify a string by replacing letters and numbers with respective agar symbols."""
    ulist = []

    for char in line:
        if char == ' ':
            ulist.append(ord(' '))
        elif char in string.ascii_uppercase:
            ulist.append(random.choice(AGAR_ALPHABETS)[ord(char) - ord('A')])
        elif char in string.digits:
            ulist.append(random.choice(AGAR_NUMBERS)[int(char)])
        else:
            ulist.append(random.choice(AGAR_SYMBOLS))

    return ulist


def generate_symbols():
    """Generates 0-2 symbols, with 0 being more likely than 1 or 2."""
    r = random.randint(1, 100)
    if r > 50:
        return []
    elif r > 25:
        return [random.choice(AGAR_SYMBOLS)]
    else:
        return random.sample(AGAR_SYMBOLS, 2)


def agarify(line, add_clan=False):
    """Agarifies a string.
    Thanks Meew (https://gist.github.com/meew0/d6c02cd156ad84869d58)
    """
    ulist = agar_replace(line.upper())

    # Add symbols randomly at the beginning and end
    ulist = generate_symbols() + ulist
    ulist = ulist + generate_symbols()

    if add_clan:
        # Add the clan at the beginning
        ulist = agar_clan() + ulist
        # Rarely, add the clan again at the end
        ulist += agar_clan() if random.randint(1, 100) <= 15 else []

    # Translate the unicode code points and return a string
    return ''.join(chr(u) for u in ulist)


AGAR_ALPHABETS = [
    # Exclude the boxed letters because they can look weird in Discord
    # [9398, 9399, 9400, 9401, 9402, 9403, 9404, 9405, 9406, 9407, 9408, 9409, 9410, 9411, 9412, 9413, 9414, 9415, 9416, 9417, 9418, 9419, 9420, 9421, 9422, 9423],
    # [9424, 9425, 9426, 9427, 9428, 9429, 9430, 9431, 9432, 9433, 9434, 9435, 9436, 9437, 9438, 9439, 9440, 9441, 9442, 9443, 9444, 9445, 9446, 9447, 9448, 9449],
    [945, 1074, 162, 8706, 1108, 402, 103, 1085, 953, 1504, 1082, 8467, 1084, 951, 963, 961, 113, 1103, 1109, 1090, 965, 957, 969, 967, 1091, 122],
    [65313, 65314, 65315, 65316, 65317, 65318, 65319, 65320, 65321, 65322, 65323, 65324, 65325, 65326, 65327, 65328, 65329, 65330, 65331, 65332, 65333, 65334, 65335, 65336, 65337, 65338],
    [65345, 65346, 65347, 65348, 65349, 65350, 65351, 65352, 65353, 65354, 65355, 65356, 65357, 65358, 65359, 65360, 65361, 65362, 65363, 65364, 65365, 65366, 65367, 65368, 65369, 65370],
    [5609, 5623, 5205, 5610, 5620, 5556, 484, 5500, 5029, 5262, 5845, 5290, 5616, 5198, 5597, 5229, 586, 5511, 5397, 19973, 5196, 5167, 5615, 5741, 435, 437],
    [916, 946, 262, 272, 8364, 8497, 5046, 294, 407, 308, 1180, 321, 924, 327, 216, 420, 937, 344, 350, 358, 7918, 86, 372, 1046, 165, 381],
    [3588, 3666, 962, 3668, 1108, 358, 65262, 1106, 3648, 1503, 1082, 108, 3667, 3616, 3663, 1511, 7907, 1075, 3619, 116, 3618, 1513, 3628, 1488, 1509, 122],
    [945, 1074, 99, 8706, 949, 1171, 103, 1085, 953, 1504, 1082, 8467, 1084, 951, 963, 961, 113, 1103, 115, 1090, 965, 118, 969, 120, 1199, 122],
    [940, 1074, 962, 273, 941, 1171, 291, 295, 943, 1112, 311, 315, 1084, 942, 972, 961, 113, 341, 351, 355, 249, 957, 974, 120, 1095, 382],
    [195, 946, 268, 270, 7864, 401, 286, 292, 302, 308, 1036, 313, 1019, 327, 7894, 420, 490, 344, 348, 356, 471, 1142, 372, 1046, 1038, 379],
    [120094, 120095, 120096, 120097, 120098, 120099, 120100, 120101, 120102, 120103, 120104, 120105, 120106, 120107, 120108, 120109, 120110, 120111, 120112, 120113, 120114, 120115, 120116, 120117, 120118, 120119],
    [120042, 120043, 120044, 120045, 119942, 119943, 120048, 120049, 120050, 120051, 120052, 120053, 120054, 120055, 120056, 120057, 120058, 120059, 120060, 120061, 120062, 120063, 120064, 120065, 120066, 120067],
    [119990, 119991, 119992, 119993, 119890, 119995, 119892, 119997, 119998, 119999, 120000, 120001, 120002, 120003, 119900, 120005, 120006, 120007, 120008, 120009, 120010, 120011, 120012, 120013, 120014, 120015],
    [120016, 120017, 120018, 120019, 120020, 120021, 120022, 120023, 120024, 120025, 120026, 120027, 120028, 120029, 120030, 120031, 120032, 120033, 120034, 120035, 120036, 120037, 120038, 120039, 120040, 120041],
    [119808, 119809, 119810, 119811, 119812, 119813, 119814, 119815, 119816, 119817, 119818, 119819, 119820, 119821, 119822, 119823, 119824, 119825, 119826, 119827, 119828, 119829, 119830, 119831, 119832, 119833],
    [119834, 119835, 119836, 119837, 119838, 119839, 119840, 119841, 119842, 119843, 119844, 119845, 119846, 119847, 119848, 119849, 119850, 119851, 119852, 119853, 119854, 119855, 119856, 119857, 119858, 119859],
    [120120, 120121, 8450, 120123, 120124, 120125, 120126, 8461, 120128, 120129, 120130, 120131, 120132, 8469, 120134, 8473, 8474, 8477, 120138, 120139, 120140, 120141, 120142, 120143, 120144, 8484],
    [120146, 120147, 120148, 120149, 120150, 120151, 120152, 120153, 120154, 120155, 120156, 120157, 120158, 120159, 120160, 120161, 120162, 120163, 120164, 120165, 120166, 120167, 120168, 120169, 120170, 120171],
    [7491, 7495, 7580, 7496, 7497, 7584, 7501, 688, 7588, 690, 7503, 737, 7504, 7600, 7506, 7510, 7520, 691, 738, 7511, 7512, 7515, 695, 739, 696, 7611],
    [592, 113, 596, 112, 477, 607, 387, 613, 33, 638, 670, 1503, 623, 117, 111, 100, 98, 633, 115, 647, 110, 652, 653, 120, 654, 122]
]
AGAR_NUMBERS = [
    [65296, 65297, 65298, 65299, 65300, 65301, 65302, 65303, 65304, 65305],
    [216, 10102, 10103, 10104, 10105, 10106, 10107, 10108, 10109, 10110],
    [7894, 10112, 10113, 10114, 10115, 10116, 10117, 10118, 10119, 10120]
]

AGAR_PARENS = [
    [65288, 65289],
    [12304, 12305],
    [12310, 12311],
    [12312, 12313],
    [12314, 12315],
    [8810, 8811],
    [8826, 8827],
    [8828, 8829],
    [8830, 8831],
    [8924, 8925],
    [8926, 8927],
    [8912, 8913],
    [8834, 8835],
    [8847, 8848],
    [8849, 8850],
    [9790, 9789],
    [2919, 2920],
    [12298, 12299],
    [10999, 11000],
    [440, 439],
    [10094, 10095],
    [10096, 10097],
    [10100, 10101],
    [5547, 5549],
    [5652, 5653],
    [8261, 8262],
    [9654, 9664],
    [9655, 9665]
]

AGAR_LETTERLIKE = [
    8450, 8461, 8469, 8473, 8474, 8477, 8484, 11362, 11363, 425, 400, 423, 424, 8475, 8476, 581, 8455, 415, 398, 423,
    404, 1048, 926, 931, 1071, 1021, 5096, 5107, 5066, 7438, 8362, 162, 353, 164, 223, 631, 926, 931, 1120, 1138, 1150,
    65505, 65509, 65510, 8362, 8486, 8492, 8475, 11363
]

AGAR_SYMBOLS = [
    65281, 65282, 65283, 65284, 65285, 65286, 65287, 65290, 65291, 65292, 65293, 10023, 65295, 65306,
    65307, 65308, 65309, 65310, 65311, 65312, 65339, 65340, 65341, 65375, 65376, 65131, 59244,
    9812, 9813, 9814, 9815, 9816, 9817, 9818, 9819, 9820, 9821, 9822, 9823, 9824, 9825, 9826, 9827, 9828, 9829, 9830, 9831, 9832, 9833, 9834, 9836, 9733, 9734,
    9618, 9619, 9608, 9607, 9606, 9605, 9604, 9603, 9602, 9601, 9754, 9755, 9756, 9757, 9758, 9759, 9760, 9762, 9774, 9775, 9785, 9786,
    8482, 174, 169, 171, 187, 5835, 8224, 8225, 9973, 9994, 9995, 9996, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032, 10022,
    10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10041, 10042, 10043, 10044, 10045, 10046, 10047, 10048, 10049, 10050, 10051, 10052,
    1757, 1758, 1769, 2794, 3024, 3303, 3313, 3424, 7461, 12484,
    526, 527, 664, 1835, 3526, 3471, 3572, 4034, 9996, 4036, 4037, 4039, 4040, 4041, 4042, 9685, 8255,
    9803, 9807, 9792, 9794, 50883, 9504, 9512, 9568, 9571,
    9609, 9610, 9611, 9612, 9613, 9614, 9615, 9616, 9620, 9621, 9632, 9644, 9600, 9604, 9680, 9681, 9682, 9683, 9703, 9704, 9705, 9706,
    9770, 9773,
    128526, 128541, 128514, 128520, 128545, 128562, 128563, 127828, 127839, 127849, 127875, 127876, 127877, 128035, 128036, 128077, 128074, 128123, 128125, 128110, 128142, 128139, 128099, 128128, 128162, 128293,
    128574, 128570, 127827, 127799, 127847, 127850, 127851, 127852, 127853, 127854, 127880, 127881, 127872, 127873, 127942, 127919, 128040, 128032, 128031, 128039, 128013, 128076, 128058, 128059, 128060, 128047,
    9986, 9988, 9989, 9998, 9999, 10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009, 10010, 10011, 10012, 10013, 10014, 10015, 10016, 10017, 10018, 10019, 10020,
    128025, 128009, 128010, 128018, 128029, 128028, 128026, 128050, 128051, 128056, 128081, 128121, 128122, 128100, 128178, 128163, 128153, 128154, 128155, 128156, 128157, 128151, 128152, 128158, 128148, 128165
]
