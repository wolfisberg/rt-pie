import mir_eval


def convert_cent_to_hz(cent, fref=10.0):
    return fref * 2 ** (cent / 1200.0)


def convert_hz_to_cent(herz, fref=10.0):
    return mir_eval.melody.hz2cents(herz, fref)


def convert_semitone_to_hz(semi, fref=10.0):
    return convert_cent_to_hz(100 * semi, fref)

