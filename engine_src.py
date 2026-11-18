import json,os,sys,urllib.request
E=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env")
INF=10**9;MATE=100000;LIM=75000
MV=[82,337,365,477,1025,0];EV=[94,281,297,512,936,0]
TP=[0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5,0,0,0,0,0,0,0,0]
TN=[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50]
TB=[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20]
TM=[-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20]
TE=[-50,-40,-30,-20,-20,-30,-40,-50,-30,-20,-10,0,0,-10,-20,-30,-30,-10,20,30,30,20,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,20,30,30,20,-10,-30,-30,-30,0,0,0,0,-30,-30,-50,-30,-30,-30,-30,-30,-30,-50]
TAB=[TP,TN,TB]
SQ=[(r<<4)|f for r in range(8) for f in range(8)]
WI=[(7-(s>>4))*8+(s&7) for s in SQ]
BI=[(s>>4)*8+(s&7) for s in SQ]
KN=[-33,-31,-18,-14,14,18,31,33];KI=[-17,-16,-15,-1,1,15,16,17]
BD=[-17,-15,15,17];RD=[-16,-1,1,16]
VAL=[0,100,320,330,500,900,0]
_z=0x243F6A8885A308D3
def _rnd():
    global _z;_z=(_z*6364136223846793005+1442695040888963407)&((1<<64)-1);return _z
ZK=[[_rnd() for _ in range(128)] for _ in range(12)]
ZS=_rnd();ZC=[_rnd() for _ in range(16)];ZE=[_rnd() for _ in range(8)]
b=[0]*128;turn=1;cast=0;ep=-1;half=0;h=0;wk=4;bk=116
TT={};N=[0];KIL=[[0,0] for _ in range(128)];HIS=[0]*32768
PH=[0,1,1,2,4,0]
def zi(v): return (abs(v)-1)*2+(v<0)
def zhash():
    x=0
    for s in SQ:
        v=b[s]
        if v: x^=ZK[zi(v)][s]
    if turn<0: x^=ZS
    x^=ZC[cast]
    if ep>=0: x^=ZE[ep&7]
    return x
def setup(fen):
    global b,turn,cast,ep,half,h,wk,bk
    b=[0]*128;p=fen.split();r=7;f=0
    for c in p[0]:
        if c=='/': r-=1;f=0
        elif c.isdigit(): f+=int(c)
        else:
            v='PNBRQK'.index(c.upper())+1;b[r*16+f]=v if c.isupper() else -v;f+=1
    turn=1 if p[1]=='w' else -1;cast=0
    if len(p)>2:
        for c in p[2]:
            if c=='K': cast|=1
            elif c=='Q': cast|=2
            elif c=='k': cast|=4
            elif c=='q': cast|=8
    ep=-1
    if len(p)>3 and p[3]!='-': ep=(int(p[3][1])-1)*16+ord(p[3][0])-97
    half=int(p[4]) if len(p)>4 else 0
    wk=next(s for s in SQ if b[s]==6);bk=next(s for s in SQ if b[s]==-6)
    NP[0]=sum(1 for s in SQ if b[s] and 1<abs(b[s])<6)
    h=zhash()
def make(m):
    global turn,cast,ep,half,h,wk,bk
    f=m&127;t=(m>>7)&127;pr=(m>>14)&7;p=b[f];cap=b[t]
    u=(m,cap,cast,ep,half,h)
    if cap and abs(cap)>1: NP[0]-=1
    if pr: NP[0]+=1
    h^=ZK[zi(p)][f]
    if cap: h^=ZK[zi(cap)][t]
    epc=0
    if abs(p)==1 and t==ep and not cap:
        cs=t-16*turn;epc=b[cs];b[cs]=0;h^=ZK[zi(epc)][cs]
    if abs(p)==6 and abs(t-f)==2:
        if t>f: rs,rd=f+3,f+1
        else: rs,rd=f-4,f-1
        r=b[rs];b[rd]=r;b[rs]=0;h^=ZK[zi(r)][rs]^ZK[zi(r)][rd]
        if turn>0: wk=t
        else: bk=t
    elif abs(p)==6:
        if turn>0: wk=t
        else: bk=t
    b[t]=pr*turn if pr else p;b[f]=0;h^=ZK[zi(b[t])][t]
    h^=ZC[cast]
    if abs(p)==6: cast&=~3 if turn>0 else ~12
    if f==7 or t==7: cast&=~1
    if f==0 or t==0: cast&=~2
    if f==119 or t==119: cast&=~4
    if f==112 or t==112: cast&=~8
    h^=ZC[cast]
    if ep>=0: h^=ZE[ep&7]
    ep=t-16*turn if abs(p)==1 and abs(t-f)==32 else -1
    if ep>=0: h^=ZE[ep&7]
    half=0 if abs(p)==1 or cap or epc else half+1
    h^=ZS;turn=-turn
    return u
def unmake(u):
    global turn,cast,ep,half,h,wk,bk
    m,cap,ocast,oep,ohalf,oh=u
    f=m&127;t=(m>>7)&127;pr=(m>>14)&7
    turn=-turn
    if abs(b[t])==6 and abs(t-f)==2:
        if t>f: b[f+3]=b[f+1];b[f+1]=0
        else: b[f-4]=b[f-1];b[f-1]=0
        if turn>0: wk=f
        else: bk=f
    elif abs(b[t])==6:
        if turn>0: wk=f
        else: bk=f
    if pr: b[f]=turn
    else: b[f]=b[t]
    b[t]=cap
    if cap and abs(cap)>1: NP[0]+=1
    if pr: NP[0]-=1
    if abs(b[f])==1 and t==oep and not cap: b[t-16*turn]=-turn
    cast,ep,half,h=ocast,oep,ohalf,oh
def atk(s,by):
    if by>0:
        for d in (-15,-17):
            t=s+d
            if not (t&0x88) and b[t]==1: return True
    else:
        for d in (15,17):
            t=s+d
            if not (t&0x88) and b[t]==-1: return True
    for d in KN:
        t=s+d
        if not (t&0x88) and b[t]==2*by: return True
    for d in KI:
        t=s+d
        if not (t&0x88) and b[t]==6*by: return True
    for d in BD:
        t=s+d
        while not (t&0x88):
            v=b[t]
            if v:
                if v==3*by or v==5*by: return True
                break
            t+=d
    for d in RD:
        t=s+d
        while not (t&0x88):
            v=b[t]
            if v:
                if v==4*by or v==5*by: return True
                break
            t+=d
    return False
def gen(caps=False):
    ms=[]
    for s in SQ:
        p=b[s]
        if not p or (p>0)!=(turn>0): continue
        a=abs(p)
        if a==1:
            d=16*turn;t=s+d
            if not (t&0x88) and not b[t] and not caps:
                lr=7 if turn>0 else 0
                if (t>>4)==lr:
                    for pr in (5,4,3,2): ms.append(s|(t<<7)|(pr<<14))
                else:
                    ms.append(s|(t<<7))
                    t2=s+2*d
                    if ((s>>4)==1 if turn>0 else (s>>4)==6) and not b[t2]: ms.append(s|(t2<<7))
            for dd in (d-1,d+1):
                t=s+dd
                if t&0x88: continue
                v=b[t]
                if v and (v>0)!=(turn>0):
                    lr=7 if turn>0 else 0
                    if (t>>4)==lr:
                        for pr in (5,4,3,2): ms.append(s|(t<<7)|(pr<<14))
                    else: ms.append(s|(t<<7))
                elif t==ep: ms.append(s|(t<<7))
        elif a==2:
            for dd in KN:
                t=s+dd
                if t&0x88: continue
                v=b[t]
                if not caps or v:
                    if not v or (v>0)!=(turn>0): ms.append(s|(t<<7))
        elif a==6:
            for dd in KI:
                t=s+dd
                if t&0x88: continue
                v=b[t]
                if not caps or v:
                    if not v or (v>0)!=(turn>0): ms.append(s|(t<<7))
            if not caps:
                if turn>0:
                    if cast&1 and not b[5] and not b[6] and b[7]==4 and not atk(4,-1) and not atk(5,-1) and not atk(6,-1): ms.append(4|(6<<7))
                    if cast&2 and not b[3] and not b[2] and not b[1] and b[0]==4 and not atk(4,-1) and not atk(3,-1) and not atk(2,-1): ms.append(4|(2<<7))
                else:
                    if cast&4 and not b[117] and not b[118] and b[119]==-4 and not atk(116,1) and not atk(117,1) and not atk(118,1): ms.append(116|(118<<7))
                    if cast&8 and not b[115] and not b[114] and not b[113] and b[112]==-4 and not atk(116,1) and not atk(115,1) and not atk(114,1): ms.append(116|(114<<7))
        else:
            ds=BD if a==3 else RD if a==4 else BD+RD
            for dd in ds:
                t=s+dd
                while not (t&0x88):
                    v=b[t]
                    if not v:
                        if not caps: ms.append(s|(t<<7))
                    else:
                        if (v>0)!=(turn>0): ms.append(s|(t<<7))
                        break
                    t+=dd
    return ms
def legal(ms):
    out=[]
    for m in ms:
        u=make(m)
        if not atk(wk if turn<0 else bk,turn): out.append(m)
        unmake(u)
    return out
def ev():
    mg=eg=ph=0;wb=bb=0
    for j,s in enumerate(SQ):
        v=b[s]
        if not v: continue
        a=abs(v);ph+=PH[a-1]
        if v>0:
            mg+=MV[a-1];eg+=EV[a-1]
            if a==6: mg+=TM[WI[j]];eg+=TE[WI[j]]
            elif a<4: mg+=TAB[a-1][WI[j]];eg+=TAB[a-1][WI[j]]
            if a==3: wb+=1
        else:
            mg-=MV[a-1];eg-=EV[a-1]
            if a==6: mg-=TM[BI[j]];eg-=TE[BI[j]]
            elif a<4: mg-=TAB[a-1][BI[j]];eg-=TAB[a-1][BI[j]]
            if a==3: bb+=1
    if wb>=2: mg+=30;eg+=50
    if bb>=2: mg-=30;eg-=50
    ph=min(ph,24)
    sc=(mg*ph+eg*(24-ph))//24
    return sc if turn>0 else -sc
NP=[0];HC={}
class Abort(Exception): pass
def order(ms,tt,ply):
    def sc(m):
        if m==tt: return 1<<20
        f=m&127;t=(m>>7)&127;v=b[t]
        if v: return 10000*VAL[abs(v)]-VAL[abs(b[f])]
        if m==KIL[ply][0] or m==KIL[ply][1]: return 9000
        return HIS[(0 if turn>0 else 16384)+f*128+t]
    return sorted(ms,key=sc,reverse=True)
def qs(a,be,ply):
    N[0]+=1
    if N[0]>LIM: raise Abort
    if half>=100: return 0
    ks=wk if turn>0 else bk
    if atk(ks,-turn):
        ms=legal(gen())
        if not ms: return -MATE+ply
        bs=-INF
        for m in order(ms,0,ply):
            u=make(m);s=-qs(-be,-a,ply+1);unmake(u)
            if s>bs: bs=s
            if s>a: a=s
            if a>=be: return a
        return bs
    s=ev()
    if s>=be: return be
    if s>a: a=s
    for m in order(legal(gen(True)),0,ply):
        u=make(m);s=-qs(-be,-a,ply+1);unmake(u)
        if s>a: a=s
        if a>=be: return a
    return a
def srch(d,a,be,ply):
    global h,turn,ep
    N[0]+=1
    if N[0]>LIM: raise Abort
    if half>=100: return 0
    if ply>0 and HC.get(h,0)>=2: return 0
    if -MATE+ply>a: a=-MATE+ply
    if MATE-ply<be: be=MATE-ply
    if a>=be: return a
    ks=wk if turn>0 else bk
    inchk=atk(ks,-turn)
    if inchk: d+=1
    if d<=0: return qs(a,be,ply)
    e=TT.get(h);ttm=0
    if e:
        if e[0]>=d:
            fl,sc,mm=e[1],e[2],e[3]
            if fl==0: return sc
            if fl==1 and sc>a: a=sc
            if fl==2 and sc<be: be=sc
            if a>=be: return sc
        ttm=e[3]
    if d>=3 and not inchk and be<90000 and NP[0]>0:
        oe=ep;oh=h
        if ep>=0: h^=ZE[ep&7]
        ep=-1;h^=ZS;turn=-turn
        HC[h]=HC.get(h,0)+1
        R=2+(d>5)
        s=-srch(d-1-R,-be,-be+1,ply+1)
        HC[h]-=1
        turn=-turn;ep=oe;h=oh
        if s>=be: return be
    ms=legal(gen())
    if not ms: return -MATE+ply if inchk else 0
    orig=a;bs=-INF;bm=0
    for i,m in enumerate(order(ms,ttm,ply)):
        f=m&127;t=(m>>7)&127;cap=b[t];pr=(m>>14)&7;quiet=not cap and not pr
        u=make(m);HC[h]=HC.get(h,0)+1
        if i==0: s=-srch(d-1,-be,-a,ply+1)
        elif i>=3 and d>=3 and quiet:
            s=-srch(d-2,-a-1,-a,ply+1)
            if s>a: s=-srch(d-1,-be,-a,ply+1)
        else:
            s=-srch(d-1,-a-1,-a,ply+1)
            if s>a: s=-srch(d-1,-be,-a,ply+1)
        HC[h]-=1;unmake(u)
        if s>bs: bs=s;bm=m
        if s>a: a=s
        if a>=be:
            if quiet:
                KIL[ply][1]=KIL[ply][0];KIL[ply][0]=m
                HIS[(0 if turn>0 else 16384)+f*128+t]+=d*d
            break
    if len(TT)>600000: TT.clear()
    if a>=be: TT[h]=(d,1,a,bm)
    elif bs>orig: TT[h]=(d,0,bs,bm)
    else: TT[h]=(d,2,bs,bm)
    return bs
def root(d,a,be):
    ms=legal(gen());bs=-INF;bm=ms[0]
    for i,m in enumerate(order(ms,0,0)):
        u=make(m);HC[h]=HC.get(h,0)+1
        if i==0: s=-srch(d-1,-be,-a,1)
        else:
            s=-srch(d-1,-a-1,-a,1)
            if s>a: s=-srch(d-1,-be,-a,1)
        HC[h]-=1;unmake(u)
        if s>bs: bs=s;bm=m
        if s>a: a=s
    return bs,bm
def think(moves):
    N[0]=0;best=moves[0];bs=0
    for d in range(1,64):
        try:
            a=-INF;be=INF
            if d>=4: a=bs-30;be=bs+30
            s,bm=root(d,a,be)
            if s<=a or s>=be: s,bm=root(d,-INF,INF)
            bs,best=s,bm
        except Abort: break
    return best
def uci(m):
    f=m&127;t=(m>>7)&127;pr=(m>>14)&7
    s="abcdefgh"[f&7]+str((f>>4)+1)+"abcdefgh"[t&7]+str((t>>4)+1)
    return s+("nbrq"[pr-2] if pr else "")
def pu(u):
    f=(int(u[1])-1)*16+ord(u[0])-97;t=(int(u[3])-1)*16+ord(u[2])-97
    pr='nbrq'.index(u[4])+2 if len(u)==5 else 0
    return f|(t<<7)|(pr<<14)
def choose(g):
    global HC
    setup(g["fen"])
    setup("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    HC={}
    for u in g["moves"]:
        make(pu(u));HC[h]=HC.get(h,0)+1
    rh=h
    setup(g["fen"])
    if rh!=h: HC={}
    moves=[pu(u) for u in g["legal_moves"]]
    if len(moves)==1: return g["legal_moves"][0]
    try: m=think(moves)
    except Exception: m=moves[0]
    u=uci(m)
    return u if u in g["legal_moves"] else g["legal_moves"][0]
def post(path,body):
    req=urllib.request.Request(E+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)
    except Exception as e: sys.exit(f"{path}: {e}")
def main():
    while True:
        g=post("/game",{})
        if g.get("status")=="done": break
        while g.get("status")=="your_move":
            try: mv=choose(g)
            except Exception: mv=g["legal_moves"][0]
            g=post("/move",{"game":g["game"],"move":mv})
        print(f"game {g.get('game')}: {g.get('outcome')} by {g.get('reason')}",file=sys.stderr)
    print("done",file=sys.stderr)
if __name__=="__main__": main()
