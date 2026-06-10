#%% main_stats

ss_names = [

    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.0_OPT/R1/mout_MED15-308_v20.7.0/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.0_OPT/R1/mout_MED15-308_v20.7.0/iteration_318/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_324/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.2_OPT/R1/mout_MED15-308_v20.7.2/iteration_329/summary_stats.p',
]


lables = [

        'start (mid)',
        'mid', 
        'fwd', 
        'bck'
          
          ]

#ss_names = [
#
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.0_OPT/R1/mout_MED15-308_v20.7.0/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.2_OPT/R1/mout_MED15-308_v20.7.2/iteration_0/summary_stats.p',
#]
#
#lables = [
#
#        'start (mid)',
#        'middle', 
#        'forward', 
#        'back'
#          
#          ]
#
#ss_names = [
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.2_RUN/mout_MED15-308_v20.6.2_LD1/iteration_0/summary_stats.p',
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.0_RUN/mout_MED15-308_v20.6.0_LD2/iteration_0/summary_stats.p',
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_RUN/mout_MED15-308_v20.6.1_LD1/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_RUN/mout_MED15-308_v20.6.1_LD2/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.0_RUN/mout_MED15-308_v20.7.2_LD3/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.1_RUN/mout_MED15-308_v20.7.1_LD2/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.2_RUN/mout_MED15-308_v20.7.2_LD2/iteration_0/summary_stats.p',
#    
#
##    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_RUN/mout_MED15-308_v20.6.1_LD3/iteration_0/summary_stats.p',
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.1_RUN/mout_MED15-308_v20.7.1_LD1/iteration_0/summary_stats.p',
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.1_RUN/mout_MED15-308_v20.7.1_LD4/iteration_0/summary_stats.p'    
#]
#
#lables = [
#
#        'start (forw)',
#        'middle', 
#        'forward', 
#        'back'
#          
#          ]
#
#
#ss_names = [
#
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.5/iteration_0/summary_stats.p',
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v32.1.0_BWOPT/mout_MED15-308_v30.2.4/iteration_0/summary_stats.p',
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.3/iteration_400/summary_stats.p',
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.4/iteration_200/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.5/iteration_500/summary_stats.p',
#    
#    ]
#
#lables = [
#        'BOPT_start',
#        'BOPT_struct_start',
#        'BOPT_NoTSR_I',
#        'BOPT_NoTSR_II',
#        'BOPT_TSR'
#          ]
#
##ss_names = [
##
##    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v32.1.0_BWOPT/mout_MED15-308_v30.2.4/iteration_0/summary_stats.p',
##    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v32.1.0_BWOPT/mout_MED15-308_v30.2.4/iteration_250/summary_stats.p',
##    
##    ]
##
##lables = [
##        'StructOpt_it0',
##        'StructOpt_it250',
##          ]
#
ss_names = [

    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.6/mout_MED15-308_v30.1.5/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.6/mout_MED15-308_v30.1.6/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.6/mout_MED15-308_v30.1.7/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.6/mout_MED15-308_v30.1.8/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.6/mout_MED15-308_v30.1.9/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.6/mout_MED15-308_v30.1.10/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.6/mout_MED15-308_v30.1.11/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.6/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.0_BOPTNSS/mout_MED15-308_v30.2.6/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.0_BOPTNSS/mout_MED15-308_v30.2.6/iteration_283/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.2_BOPTSTR/iteration_241/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.4_BOPTSTR/iteration_125/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.6_BOPTSTR/iteration_158/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.8_BOPTNSS/iteration_0/summary_stats.p',
    
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.8_BOPTNSS/iteration_116/summary_stats.p',
    
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.8_BOPTNSS/iteration_81/summary_stats.p',
    
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.11/iteration_0/summary_stats.p',
    
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.13/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/MED15-308_v30.2.7_BOPSTD/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.13/iteration_176/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.11/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.14/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.15/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.17/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.16/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.11_BOPTSTR/mout_MED15-308_v30.2.11/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.11_BOPTSTR/mout_MED15-308_v30.2.12/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.0_BOPTSTR/mout_MED15-308_v30.3.1/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.2_BOPTSTR/mout_MED15-308_v30.3.3/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.2_BOPTNSS/mout_MED15-308_v30.3.4/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.2_BOPTNSS/mout_MED15-308_v30.3.4/iteration_46/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.20_BOPTSTR/mout_MED15-308_v30.2.21/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.11_BOPTSTR/mout_MED15-308_v30.2.12/iteration_64/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/IEA22_RWT/mout_DLC_1.6/iteration_0/summary_stats.p',
    #r'MED15-308_v30.2.11_BOPTSTR/mout_MED15-308_v30.2.11/iteration_83/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.15/iteration_209/summary_stats.p',
    
    #r'/mnt/d/RUN/AGSM/IEA_22MW/IEA22MW_RWT_PC_out/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.3_RUN/DLC16_MED15-308_v30.3.3/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.2_BOPTSTR/iteration_0/summary_stats.p', 
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.2_BOPTSTR/mout_MED15-308_v30.3.3/iteration_0/summary_stats.p', 
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.2_BOPTNSS/mout_MED15-308_v30.3.4/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.3_BOPTNSS/mout_MED15-308_v30.3.4/iteration_105/summary_stats.p',
    
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.20_BOPTSTR/mout_MED15-308_v30.2.22/iteration_0/summary_stats.p',
    
        ]
lables = [
'30.3.2_1.6_NEW',
'30.3.2_1.6_OLD',
'30.2.20_1.6',
          ]
ss_names = [
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15_308_v30.2.21_RUN/DLC_AEP_MED15-308_v30.2.21/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15_308_v30.2.21_RUN/DLC11_MED15-308_v30.2.21/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15_308_v30.2.21_RUN/DLC16_MED15-308_v30.2.21/iteration_0/summary_stats.p', 
]
lables = [
'30.2.21_AEP',
'30.2.21_DLC11',
'30.2.22_DLC16',
          ]

ss_names = [
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15_308_v30.2.21_RUN/DLC_AEP_MED15-308_v30.2.21/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.3_RUN/DLC_AEP_MED15-308_v30.3.3/iteration_0/summary_stats.p',
    ]
lables = [
'30.2.21_AEP',
'30.3.3_AEP',
          ]

ss_names = [
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15_308_v30.2.21_RUN/DLC16_MED15-308_v30.2.21/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.22_BOPTNSS/mout_MED15-308_v30.2.23/iteration_80/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.23_RUN/DLC16_MED15-308_v30.2.23/iteration_0/summary_stats.p',
    #r'/mnt/d/RUN/AGSM/IEA_22MW/IEA22MW_RWT_PC_out/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/IEA22_RWT/mout_DLC_1.6/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.23_RUN/DLC_AEP_MED15-308_v30.2.23_RTChange/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.23_RUN/DLC_AEP_MED15-308_v30.2.23/iteration_0/summary_stats.p',
    


    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.24_RUN/DLC_AEP_MED15-308_v30.2.24/iteration_0/summary_stats.p',
    #  r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.24_RUN/DLC_AEP_MED15-308_v30.2.24/iteration_0_TRY3/summary_stats.p',
     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.24_RUN/DLC_AEP_MED15-308_v30.2.24/OLD_iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.24_RUN/DLC16_MED15-308_v30.2.24/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.23_BOPTNSS/iteration_130/summary_stats.p'
    ]

lables = [
'30.2.24_AEP',
'30.2.24_DLC16',
'30.2.24_BOPTNSS',
          ]

#ss_names = [
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15_308_v30.2.21_RUN/DLC11_MED15-308_v30.2.21/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.3_RUN/DLC11_MED15-308_v30.3.3/iteration_0/summary_stats.p',
#    ]
#lables = [
#'30.2.21_DLC11',
#'30.3.3_DLC11',
#          ]
#
#ss_names = [
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15_308_v30.2.21_RUN/DLC16_MED15-308_v30.2.21/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.3_RUN/DLC16_MED15-308_v30.3.3/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/IEA22_RWT/mout_DLC_1.6/iteration_0/summary_stats.p',
#    ]
#lables = [
#'30.2.21_DLC16',
#'30.3.3_DLC16',
#'IEA22_DLC16',
#          ]

##ss_names = [
##
##    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_324/summary_stats.p',
##    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.1_RUN/mout_MED15-308_v20.7.1_LD1/iteration_0/summary_stats.p',
##    
##    ]
##
##lables = [
##        'MED-20.7.1_END_OPT',
##        'MED-20.7.1_RE-RUN',
##
##          ]

#ss_names = [
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.16/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.16/iteration_272/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.17/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.17/iteration_265/summary_stats.p', 
#
#    ]
#
#lables = [
#
#    'START THIN',
#    'END THIN',
#    'START THICK',
#    'END THICK', 
#
#    ]

#%% main TSS

# files = [
#     #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_CtrlOpt/R2/mout_MED15-308_v30.1.1/iteration_0/timeseries/MED15-308_v30.1.1_26.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_CtrlOpt/R2/mout_MED15-308_v30.1.1/iteration_115/timeseries/MED15-308_v30.1.1_26.p',

# ]

# lables = [

#         'iter_0', 
#         'iter_115'
          
#           ]

# files = [
#     #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPT/mout_MED15-308_v30.1.2/iteration_0/timeseries/MED15-308_v30.1.2_26.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPT/mout_MED15-308_v30.1.2/iteration_79/timeseries/MED15-308_v30.1.2_26.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.3/iteration_0/timeseries/MED15-308_v30.1.3_26.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.3/iteration_208/timeseries/MED15-308_v30.1.3_26.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.3/iteration_193/timeseries/MED15-308_v30.1.3_26.p',

# ]

# lables = [

#         'BOPT_it0', 
#         'BOPT_it79',
#         'BOPTNSS_it0',  
#         'BOPTNSS_it208',
#         'BOPTNSS_it193',
#           ]

# files = [
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.22_BOPTNSS/mout_MED15-308_v30.2.23/iteration_0/timeseries/MED15-308_v30.2.23_20.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.22_BOPTNSS/mout_MED15-308_v30.2.23/iteration_80/timeseries/MED15-308_v30.2.23_20.p',
# ]

# lables = [

#         'iter_0', 
#         'iter_80',
          
#           ]


#%% main span

# ss_names = [
#     #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.11_BOPTSTR/mout_MED15-308_v30.2.12/iteration_0/summary_stats.p',
#     #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.8_BOPTNSS/iteration_0/summary_stats.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.17/iteration_0/summary_stats.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.17/iteration_265/summary_stats.p',
#     #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.16/iteration_0/summary_stats.p',
#     ]

# lables = [
# 'START STEADY',
# 'END STEADY',
#           ]

# ## MED STEADY vs DLC1.1
# ss_names = [
#     #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.8_BOPTNSS/iteration_0/summary_stats.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.17/iteration_0/summary_stats.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.16/iteration_0/summary_stats.p',
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.16/iteration_272/summary_stats.p',
# ]

# lables = [
#     'STEADY THICK START',
#     'STEADY THIN START',
#     'STEADY THIN END',
# ]

# ## MED CLD1.6 vs DLC1.1 vs IEA 22  DLC 1.6
# ss_names = [
#     r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/IEA22_RWT/mout_DLC_1.6/iteration_0/summary_stats.p',
#     # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.0_BOPTSTR/mout_MED15-308_v30.3.1/iteration_0/summary_stats.p', 
#     # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.2_BOPTNSS/mout_MED15-308_v30.3.4/iteration_0/summary_stats.p',
# ]

# lables = [
#     'IEA 22',
#     'DLC THIN DLC 1.6',
#     'MED THIN DLC 1.1'
# ]
