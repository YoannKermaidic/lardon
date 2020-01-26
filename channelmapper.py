import config as cf

def check():
    if(len(cf.map_ref) > 0):
        del cf.map_ref[:]

def ChannelMapper():    
    check()
    for idaq in range(cf.n_ChanTot):
        crp, view, vchan = DAQToCRP(idaq)
        ev = cf.pdmap()
        ev.view = view
        ev.crp = crp
        ev.vchan = vchan
        cf.map_ref.append(ev)

def DAQToCRP(daqch):
    n_Crates = 12
    n_CardPerCrate = 10
    n_ChPerCard = 64
    n_ChPerCrate = n_CardPerCrate * n_ChPerCard 
    n_ChPerConnector = 8
    HalfCrate = n_Crates/2
    QuartCrate = HalfCrate/2
    HalfCard = n_CardPerCrate/2
    HalfChPerCrate = n_ChPerCrate/2
    
    crate = int(daqch/n_ChPerCrate)
    card  = int(daqch - crate * n_ChPerCrate)/n_ChPerCard
    chcard = int(daqch - crate * n_ChPerCrate - card * n_ChPerCard)
    conn   = int(chcard/n_ChPerConnector)
    view = 0 if crate < HalfCrate else 1

    crp  = -1
    
    if(view==0):
        if(crate < QuartCrate):
            if(card < HalfCard):
                crp = 1
            else:
                crp = 2
        else:
            if(card < HalfCard):
                crp = 0
            else:
                crp = 3
    else:
        if((crate-HalfCrate) < QuartCrate):
            if(card < HalfCard):
                crp = 0
            else:
                crp = 1
        else:
            if(card < HalfCard):
                crp = 3
            else:
                crp = 2
            
    vchan = -1
    if(view==0):
        vchan = abs(chcard-conn*n_ChPerConnector - 7) + conn*n_ChPerConnector + (crate%QuartCrate)*HalfChPerCrate + (card if card < HalfCard else card-HalfCard)*n_ChPerCard
    else:
        vchan = abs(chcard-conn*n_ChPerConnector - 7) + conn*n_ChPerConnector + abs((crate%QuartCrate)-2)*HalfChPerCrate + abs((card if card < HalfCard else card-HalfCard)-4)*n_ChPerCard
    return crp, view, vchan