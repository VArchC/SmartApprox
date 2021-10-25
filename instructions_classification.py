
MEMORY      = "memory"
#ARITHMETIC  = "arithmetic"
FLOW        = "flow"
LOAD        = "load"
STORE       = "store"
TOTAL       = "total"
BARRIER     = "barrier"
FP          = "floating-point"
JUMP_REG    = "jump to register"

NORM_PREAMBLE = "#NORM#_"

classification={}

classification[TOTAL] = [ "All" ]

classification[LOAD] = [
        #LOAD
            'lb',
            'lh',
            'lw',
            'lbu',
            'lhu',
            'ld',
            'lr_d',
            'lr_w',
            'lui',
            'lwu',
        #HYPERVISOR LOAD
            'hlv_b',
            'hlv_bu',
            'hlv_h',
            'hlv_hu',
            'hlv_w',
        #reserved
            'lr_w',
            'lr_d',
        #quad-word
            'lq',
        #floating point
            'fld',
            'flw',
        #register based (cs formats)
            'c_lw',
            'c_ld',
            'c_lq',
            'c_flw',
            'c_fld',
            'c_flw',
            'c_fld',
        #stack pointer based
            'c_fldsp',
            'c_flwsp',
            'c_lqsp',
            'c_ldsp',
            'c_lwsp',

        ]
classification[STORE] = [
        #STORE
            'sb',
            'sh',
            'sw',
            'sd',
            'sc_d',
            'sc_w',
        #quad-word
            'sq',
        #HYPERVISOR STORE
            'hsv_b',
            'hsv_h',
            'hsv_w',
            'hlv_wu',
        #store conditional
            'sc_w',
            'sc_d',
        #floating point
            'fsd',
            'fsw',
            'fsq',
        #register based (cs formats)
            'c_sw',
            'c_sd',
            'c_sq',
            'c_fsw',
            'c_fsd',
        #stack pointer based
            'c_swsp',
            'c_sdsp',
            'c_sqsp',
            'c_fswsp',
            'c_fsdsp',
        ]

classification[MEMORY] = classification[LOAD] + classification[STORE]
        
classification[JUMP_REG] = [
            'jalr',
            'c_jalr',
            'jr',
            'c_jr',
        ]

classification[FLOW] = [
        #JUMPS
            'jal',
            'jalr',
            'jr',
            'j',
            'c_j',
            'c_jal',
            'c_jr',
            'c_jalr',
        #BRANCHES
            'beq',
            'bne',
            'blt',
            'bltu',
            'bge',
            'bgeu',
            'bgt',
            'bgtu',
            'ble',
            'bleu',
            'c_beqz',
            'c_bnez',
        #breaks
            'ebreak',
            'c_ebreak',
        #calls
            'ecall',
            'dret',
        ]

classification[BARRIER] = [
            'fence',
            'fence_tso',
            'fence_i',
            'sfence_vma',
        ]

classification[FP] = [
            'fadd_d',
            'fadd_q',
            'fadd_s',
            'fclass_d',
            'fclass_q',
            'fclass_s',
            'fcvt_d_l',
            'fcvt_d_lu',
            'fcvt_d_q',
            'fcvt_d_s',
            'fcvt_d_w',
            'fcvt_d_wu',
            'fcvt_l_d',
            'fcvt_l_q',
            'fcvt_l_s',
            'fcvt_lu_d',
            'fcvt_lu_q',
            'fcvt_lu_s',
            'fcvt_q_d',
            'fcvt_q_l',
            'fcvt_q_lu',
            'fcvt_q_s',
            'fcvt_q_w',
            'fcvt_q_wu',
            'fcvt_s_d',
            'fcvt_s_l',
            'fcvt_s_lu',
            'fcvt_s_q',
            'fcvt_s_w',
            'fcvt_s_wu',
            'fcvt_w_d',
            'fcvt_w_q',
            'fcvt_w_s',
            'fcvt_wu_d',
            'fcvt_wu_q',
            'fcvt_wu_s',
            'fdiv_d',
            'fdiv_q',
            'fdiv_s',
            'feq_d',
            'feq_q',
            'feq_s',
            'fld',
            'fle_d',
            'fle_q',
            'fle_s',
            'flq',
            'flt_d',
            'flt_q',
            'flt_s',
            'flw',
            'fmadd_d',
            'fmadd_q',
            'fmadd_s',
            'fmax_d',
            'fmax_q',
            'fmax_s',
            'fmin_d',
            'fmin_q',
            'fmin_s',
            'fmsub_d',
            'fmsub_q',
            'fmsub_s',
            'fmul_d',
            'fmul_q',
            'fmul_s',
            'fmv_d_x',
            'fmv_w_x',
            'fmv_x_d',
            'fmv_x_w',
            'fnmadd_d',
            'fnmadd_q',
            'fnmadd_s',
            'fnmsub_d',
            'fnmsub_q',
            'fnmsub_s',
            'fsd',
            'fsgnj_d',
            'fsgnj_q',
            'fsgnj_s',
            'fsgnjn_d',
            'fsgnjn_q',
            'fsgnjn_s',
            'fsgnjx_d',
            'fsgnjx_q',
            'fsgnjx_s',
            'fsq',
            'fsqrt_d',
            'fsqrt_q',
            'fsqrt_s',
            'fsub_d',
            'fsub_q',
            'fsub_s',
            'fsw',
        ]
