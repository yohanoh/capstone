def importance(cblockLIst):
    bigsize = 0
    big_cblock = cblockLIst[0]

    for cblock in cblockLIst:
        size = cblock.getHeight() * cblock.getWidth()

        if size > bigsize:
            bigsize = size
            big_cblock = cblock

    return big_cblock
