#helper to make skin xml file 


if 1==11:
    initx=60
    inity=130
    xpos= {0:0,  1:200,2:400}
    width={0:200,1:200,2:600}
    yposincr=100
    height=70
    
    for h in range(3):
        print ' '
        for i in range(len(xpos)):
            print '<control type="label" id="%d">'%(1000+(h*1000)+i)
            print ' <posx>%d</posx>'%(initx+xpos[i])
            print ' <posy>%d</posy>'%(inity+h*yposincr)
            print ' <width>%d</width>'%(width[i])
            print ' <height>%d</height>'%(height)
            print ' <font>font45caps_title</font>'
            print ' <aligny>center</aligny>'
            print ' <label></label>'
            print '</control>'

