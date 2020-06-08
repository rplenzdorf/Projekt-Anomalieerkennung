def erkennung(p,t):
    if p(t) < 50:
        anom = True
    else:
        anom = False

    return anom