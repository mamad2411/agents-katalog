# Rewritten by CleanModels 3 Version 3.7.0 [990e9a0] Sat Mar 01 22:13:28 2025
#MAXMODEL ASCII
filedependency Unknown
newmodel ctl_cg_btn_skill
        setsupermodel ctl_cg_btn_skill NULL
        setanimationscale 1
#MAXGEOM ASCII
beginmodelgeom ctl_cg_btn_skill
    node dummy ctl_cg_btn_skill
        parent NULL
    endnode
    node dummy icon
        parent ctl_cg_btn_skill
        position 0.21 0.21 0.05
        orientation 0 0 0 0
    endnode
    node dummy text0
        parent ctl_cg_btn_skill
        position 0.43 0.37 0.1
        orientation 0 0 0 0
    endnode
    node dummy next
        parent ctl_cg_btn_skill
        position 0 -0.44 0
        orientation 0 0 0 0
    endnode
    node dummy skillup
        parent ctl_cg_btn_skill
        position 2.95 0.135 1
        orientation 0 0 0 0
    endnode
    node dummy skilldown
        parent ctl_cg_btn_skill
        position 2.6 0.135 1
        orientation 0 0 0 0
    endnode
    node animmesh plane217
        parent ctl_cg_btn_skill
        ambient 0.0640517 0.186926 0.128103
        diffuse 1 1 1
        specular 0.045 0.045 0.045
        shininess 26
        bitmap ctl_skill
        position 1.62 0.21 -0.03
        orientation 0 0 0 0
        sampleperiod 0
        verts 4
            -1.62 0.21 0
            -1.62 -0.21 0
            1.62 0.21 0
            1.62 -0.21 0
        faces 2
            0 1 2 1 0 1 2 1
            3 2 1 1 3 2 1 1
        tverts 4
            0.183594 1.00781 0
            0.183594 0.679688 0
            0.816406 1.00781 0
            0.816406 0.679687 0
    endnode
    node dummy skillrank
        parent ctl_cg_btn_skill
        position 2.06 0.03 0
        orientation 0 0 0 0
    endnode
    node dummy text1
        parent ctl_cg_btn_skill
        position 2.62 0.03 0.1
        orientation 0 0 0 0
    endnode
endmodelgeom ctl_cg_btn_skill

#MAXANIM ASCII
newanim checkeddown ctl_cg_btn_skill
        length 1
        transtime 0
        animroot ctl_cg_btn_skill
        node dummy ctl_cg_btn_skill
            parent NULL
        endnode
        node dummy icon
            parent ctl_cg_btn_skill
        endnode
        node dummy text0
            parent ctl_cg_btn_skill
            positionkey
      0 0.43 0.360002 0.1
      1 0.43 0.36 0.1
            endlist
        endnode
        node dummy next
            parent ctl_cg_btn_skill
        endnode
        node dummy skillup
            parent ctl_cg_btn_skill
        endnode
        node dummy skilldown
            parent ctl_cg_btn_skill
        endnode
        node animmesh plane217
            parent ctl_cg_btn_skill
            sampleperiod 1
            verts 4
            -1.62 0.21 0
            -1.62 -0.21 0
            1.62 0.21 0
            1.62 -0.21 0
            faces 2
            0 1 2 1 0 1 2 1
            3 2 1 1 3 2 1 1
            tverts 4
            0.183594 1.00781 0
            0.183594 0.679688 0
            0.816406 1.00781 0
            0.816406 0.679687 0
            animverts 4
      -1.62 0.21 0
      -1.62 -0.21 0
      1.62 0.21 0
      1.62 -0.21 0
            animtverts 4
      0.183594 0.671877 0
      0.183594 0.343752 0
      0.816406 0.671876 0
      0.816406 0.343751 0
        endnode
        node dummy skillrank
            parent ctl_cg_btn_skill
        endnode
        node dummy text1
            parent ctl_cg_btn_skill
        endnode
doneanim checkeddown ctl_cg_btn_skill

#MAXANIM ASCII
newanim checkedup ctl_cg_btn_skill
        length 1
        transtime 0
        animroot ctl_cg_btn_skill
        node dummy ctl_cg_btn_skill
            parent NULL
        endnode
        node dummy icon
            parent ctl_cg_btn_skill
        endnode
        node dummy text0
            parent ctl_cg_btn_skill
            positionkey
      0 0.43 0.37 0.1
      1 0.43 0.37 0.1
            endlist
        endnode
        node dummy next
            parent ctl_cg_btn_skill
        endnode
        node dummy skillup
            parent ctl_cg_btn_skill
        endnode
        node dummy skilldown
            parent ctl_cg_btn_skill
        endnode
        node animmesh plane217
            parent ctl_cg_btn_skill
            sampleperiod 1
            verts 4
            -1.62 0.21 0
            -1.62 -0.21 0
            1.62 0.21 0
            1.62 -0.21 0
            faces 2
            0 1 2 1 0 1 2 1
            3 2 1 1 3 2 1 1
            tverts 4
            0.183594 1.00781 0
            0.183594 0.679688 0
            0.816406 1.00781 0
            0.816406 0.679687 0
            animverts 4
      -1.62 0.21 0
      -1.62 -0.21 0
      1.62 0.21 0
      1.62 -0.21 0
            animtverts 4
      0.183594 0.671876 0
      0.183594 0.343751 0
      0.816406 0.671875 0
      0.816406 0.34375 0
        endnode
        node dummy skillrank
            parent ctl_cg_btn_skill
        endnode
        node dummy text1
            parent ctl_cg_btn_skill
        endnode
doneanim checkedup ctl_cg_btn_skill

#MAXANIM ASCII
newanim disabled ctl_cg_btn_skill
        length 1
        transtime 0
        animroot ctl_cg_btn_skill
        node dummy ctl_cg_btn_skill
            parent NULL
        endnode
        node dummy icon
            parent ctl_cg_btn_skill
        endnode
        node dummy text0
            parent ctl_cg_btn_skill
            positionkey
      0 0.43 0.37 0.1
            endlist
        endnode
        node dummy next
            parent ctl_cg_btn_skill
        endnode
        node dummy skillup
            parent ctl_cg_btn_skill
        endnode
        node dummy skilldown
            parent ctl_cg_btn_skill
        endnode
        node animmesh plane217
            parent ctl_cg_btn_skill
            sampleperiod 1
            verts 4
            -1.62 0.21 0
            -1.62 -0.21 0
            1.62 0.21 0
            1.62 -0.21 0
            faces 2
            0 1 2 1 0 1 2 1
            3 2 1 1 3 2 1 1
            tverts 4
            0.183594 1.00781 0
            0.183594 0.679688 0
            0.816406 1.00781 0
            0.816406 0.679687 0
            animverts 4
      -1.62 0.21 0
      -1.62 -0.21 0
      1.62 0.21 0
      1.62 -0.21 0
            animtverts 4
      0.183594 1.00781 0
      0.183594 0.679687 0
      0.816406 1.00781 0
      0.816406 0.679687 0
        endnode
        node dummy skillrank
            parent ctl_cg_btn_skill
        endnode
        node dummy text1
            parent ctl_cg_btn_skill
        endnode
doneanim disabled ctl_cg_btn_skill

#MAXANIM ASCII
newanim down ctl_cg_btn_skill
        length 1
        transtime 0
        animroot ctl_cg_btn_skill
        node dummy ctl_cg_btn_skill
            parent NULL
        endnode
        node dummy icon
            parent ctl_cg_btn_skill
        endnode
        node dummy text0
            parent ctl_cg_btn_skill
            positionkey
      0 0.43 0.360002 0.1
      1 0.43 0.36 0.1
            endlist
        endnode
        node dummy next
            parent ctl_cg_btn_skill
        endnode
        node dummy skillup
            parent ctl_cg_btn_skill
        endnode
        node dummy skilldown
            parent ctl_cg_btn_skill
        endnode
        node animmesh plane217
            parent ctl_cg_btn_skill
            sampleperiod 1
            verts 4
            -1.62 0.21 0
            -1.62 -0.21 0
            1.62 0.21 0
            1.62 -0.21 0
            faces 2
            0 1 2 1 0 1 2 1
            3 2 1 1 3 2 1 1
            tverts 4
            0.183594 1.00781 0
            0.183594 0.679688 0
            0.816406 1.00781 0
            0.816406 0.679687 0
            animverts 4
      -1.62 0.21 0
      -1.62 -0.21 0
      1.62 0.21 0
      1.62 -0.21 0
            animtverts 4
      0.183594 0.671877 0
      0.183594 0.343752 0
      0.816406 0.671876 0
      0.816406 0.343751 0
        endnode
        node dummy skillrank
            parent ctl_cg_btn_skill
        endnode
        node dummy text1
            parent ctl_cg_btn_skill
        endnode
doneanim down ctl_cg_btn_skill

#MAXANIM ASCII
newanim hilite ctl_cg_btn_skill
        length 1
        transtime 0
        animroot ctl_cg_btn_skill
        node dummy ctl_cg_btn_skill
            parent NULL
        endnode
        node dummy icon
            parent ctl_cg_btn_skill
        endnode
        node dummy text0
            parent ctl_cg_btn_skill
        endnode
        node dummy next
            parent ctl_cg_btn_skill
        endnode
        node dummy skillup
            parent ctl_cg_btn_skill
        endnode
        node dummy skilldown
            parent ctl_cg_btn_skill
        endnode
        node animmesh plane217
            parent ctl_cg_btn_skill
            sampleperiod 1
            verts 4
            -1.62 0.21 0
            -1.62 -0.21 0
            1.62 0.21 0
            1.62 -0.21 0
            faces 2
            0 1 2 1 0 1 2 1
            3 2 1 1 3 2 1 1
            tverts 4
            0.183594 1.00781 0
            0.183594 0.679688 0
            0.816406 1.00781 0
            0.816406 0.679687 0
            animverts 4
      -1.62 0.21 0
      -1.62 -0.21 0
      1.62 0.21 0
      1.62 -0.21 0
            animtverts 4
      0.183594 0.335938 0
      0.183594 0.0078128 0
      0.816406 0.335937 0
      0.816406 0.0078122 0
        endnode
        node dummy skillrank
            parent ctl_cg_btn_skill
        endnode
        node dummy text1
            parent ctl_cg_btn_skill
        endnode
doneanim hilite ctl_cg_btn_skill

#MAXANIM ASCII
newanim uncheckeddown ctl_cg_btn_skill
        length 1
        transtime 0
        animroot ctl_cg_btn_skill
        node dummy ctl_cg_btn_skill
            parent NULL
        endnode
        node dummy icon
            parent ctl_cg_btn_skill
        endnode
        node dummy text0
            parent ctl_cg_btn_skill
            positionkey
      0 0.43 0.35999 0.1
      1 0.43 0.36 0.1
            endlist
        endnode
        node dummy next
            parent ctl_cg_btn_skill
        endnode
        node dummy skillup
            parent ctl_cg_btn_skill
        endnode
        node dummy skilldown
            parent ctl_cg_btn_skill
        endnode
        node animmesh plane217
            parent ctl_cg_btn_skill
            sampleperiod 1
            verts 4
            -1.62 0.21 0
            -1.62 -0.21 0
            1.62 0.21 0
            1.62 -0.21 0
            faces 2
            0 1 2 1 0 1 2 1
            3 2 1 1 3 2 1 1
            tverts 4
            0.183594 1.00781 0
            0.183594 0.679688 0
            0.816406 1.00781 0
            0.816406 0.679687 0
            animverts 4
      -1.62 0.21 0
      -1.62 -0.21 0
      1.62 0.21 0
      1.62 -0.21 0
            animtverts 4
      0.183594 1.00781 0
      0.183594 0.679689 0
      0.816406 1.00781 0
      0.816406 0.679688 0
        endnode
        node dummy skillrank
            parent ctl_cg_btn_skill
        endnode
        node dummy text1
            parent ctl_cg_btn_skill
        endnode
doneanim uncheckeddown ctl_cg_btn_skill

#MAXANIM ASCII
newanim uncheckedup ctl_cg_btn_skill
        length 1
        transtime 0
        animroot ctl_cg_btn_skill
        node dummy ctl_cg_btn_skill
            parent NULL
        endnode
        node dummy icon
            parent ctl_cg_btn_skill
        endnode
        node dummy text0
            parent ctl_cg_btn_skill
            positionkey
      1 0.43 0.37 0.1
            endlist
        endnode
        node dummy next
            parent ctl_cg_btn_skill
        endnode
        node dummy skillup
            parent ctl_cg_btn_skill
        endnode
        node dummy skilldown
            parent ctl_cg_btn_skill
        endnode
        node animmesh plane217
            parent ctl_cg_btn_skill
            sampleperiod 1
            verts 4
            -1.62 0.21 0
            -1.62 -0.21 0
            1.62 0.21 0
            1.62 -0.21 0
            faces 2
            0 1 2 1 0 1 2 1
            3 2 1 1 3 2 1 1
            tverts 4
            0.183594 1.00781 0
            0.183594 0.679688 0
            0.816406 1.00781 0
            0.816406 0.679687 0
            animverts 4
      -1.62 0.21 0
      -1.62 -0.21 0
      1.62 0.21 0
      1.62 -0.21 0
            animtverts 4
      0.183594 1.00781 0
      0.183594 0.679688 0
      0.816406 1.00781 0
      0.816406 0.679688 0
        endnode
        node dummy skillrank
            parent ctl_cg_btn_skill
        endnode
        node dummy text1
            parent ctl_cg_btn_skill
        endnode
doneanim uncheckedup ctl_cg_btn_skill

#MAXANIM ASCII
newanim up ctl_cg_btn_skill
        length 1
        transtime 0
        animroot ctl_cg_btn_skill
        node dummy ctl_cg_btn_skill
            parent NULL
        endnode
        node dummy icon
            parent ctl_cg_btn_skill
        endnode
        node dummy text0
            parent ctl_cg_btn_skill
            positionkey
      1 0.43 0.37 0.1
            endlist
        endnode
        node dummy next
            parent ctl_cg_btn_skill
        endnode
        node dummy skillup
            parent ctl_cg_btn_skill
        endnode
        node dummy skilldown
            parent ctl_cg_btn_skill
        endnode
        node animmesh plane217
            parent ctl_cg_btn_skill
            sampleperiod 1
            verts 4
            -1.62 0.21 0
            -1.62 -0.21 0
            1.62 0.21 0
            1.62 -0.21 0
            faces 2
            0 1 2 1 0 1 2 1
            3 2 1 1 3 2 1 1
            tverts 4
            0.183594 1.00781 0
            0.183594 0.679688 0
            0.816406 1.00781 0
            0.816406 0.679687 0
            animverts 4
      -1.62 0.21 0
      -1.62 -0.21 0
      1.62 0.21 0
      1.62 -0.21 0
            animtverts 4
      0.183594 1.00781 0
      0.183594 0.679688 0
      0.816406 1.00781 0
      0.816406 0.679688 0
        endnode
        node dummy skillrank
            parent ctl_cg_btn_skill
        endnode
        node dummy text1
            parent ctl_cg_btn_skill
        endnode
doneanim up ctl_cg_btn_skill
donemodel ctl_cg_btn_skill
