import mir_eval


def convert_cent_to_hz(cent, f_ref=10.0):
    return f_ref * 2 ** (cent / 1200.0)


def convert_hz_to_cent(hertz, f_ref=10.0):
    return mir_eval.melody.hz2cents(hertz, f_ref)


def convert_semitone_to_hz(semi, f_ref=10.0):
    return convert_cent_to_hz(100 * semi, f_ref)
