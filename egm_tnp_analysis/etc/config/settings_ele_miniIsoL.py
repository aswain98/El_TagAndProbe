#############################################################
########## General settings
#############################################################
# flag to be Tested
#cutpass80 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.967083,0.929117,0.726311)
#cutpass90 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.913286,0.805013,0.358969)
cutpassminiIsoTight = '(passingMini == 1)'
cutpassminiIsoLoose = '(passingMini4 == 1)'
cutpassMVA94Xwp90noiso = '(passingMVA94Xwp90noisoV2 == 1)'
cutpassMVA94XwpLnoiso = '(passingMVA94XwpLnoisoV2 == 1)'

# flag to be Tested
flags = {
    'passingVeto94XV2'    : '(passingVeto94XV2   == 1)',
    'passingLoose94XV2'   : '(passingLoose94XV2  == 1)',
    'passingMedium94XV2'  : '(passingMedium94XV2 == 1)',
    'passingTight94XV2'   : '(passingTight94XV2  == 1)',
    'passingMVA94Xwp80isoV2' : '(passingMVA94XV2wp80isoV2 == 1)',
    'passingMVA94Xwp90isoV2' : '(passingMVA94Xwp90isoV2 == 1)',
    'passingMVA94XwpLnoisoV2': '(passingMVA94XwpLnoisoV2 == 1)',
    'passingMVA94Xwp80noisoV2' : '(passingMVA94Xwp80noisoV2 == 1)',
    'passingMVA94Xwp90noisoV2' : '(passingMVA94Xwp90noisoV2 == 1)',
    'passingMiniIsoTight': '(passingMini == 1)',
    'passingMiniIsoLoose': '(passingMini4 == 1)',
    }

#baseOutDir = 'results/Data2018/tnpEleID/runA/'
baseOutDir = 'results/Data2018/miniIsoTight_pTgt20/'

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpEleIDs'

samplesDef = {
    'data'   : tnpSamples.Moriond19_10X['data_Run2018A'].clone(),
    'mcNom'  : tnpSamples.Moriond19_10X['DY_madgraph'].clone(),
    'mcAlt'  : tnpSamples.Moriond19_10X['DY_madgraph'].clone(),
    'tagSel' : tnpSamples.Moriond19_10X['DY_madgraph'].clone(),
}

## can add data sample easily
samplesDef['data'].add_sample( tnpSamples.Moriond19_10X['data_Run2018B'] )
samplesDef['data'].add_sample( tnpSamples.Moriond19_10X['data_Run2018C'] )
samplesDef['data'].add_sample( tnpSamples.Moriond19_10X['data_Run2018D'] )
#samplesDef['data'].add_sample( tnpSamples.Moriond18_94X['data_Run2017F'] )

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
samplesDef['data' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 37') #canceled non trig MVA cut

## set MC weight, simple way (use tree weight) 
#weightName = 'totWeight'
#if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
#if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

## set MC weight, can use several pileup rw for different data taking periods
weightName = 'weights_2018_runABCD.totWeight'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree('/afs/cern.ch/user/w/wiwong/work/TagAndProbe/CMSSW_10_2_5/src/egm_tnp_analysis/PUTree/DY_madgraph_ele.pu.puTree.root')
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree('/afs/cern.ch/user/w/wiwong/work/TagAndProbe/CMSSW_10_2_5/src/egm_tnp_analysis/PUTree/DY_madgraph_ele.pu.puTree.root')
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree('/afs/cern.ch/user/w/wiwong/work/TagAndProbe/CMSSW_10_2_5/src/egm_tnp_analysis/PUTree/DY_madgraph_ele.pu.puTree.root')



#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
#   { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
   { 'var' : 'el_sc_abseta' , 'type': 'float', 'bins': [0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
#   { 'var' : 'el_pt' , 'type': 'float', 'bins': [10,20,35,50,100,200,500] },
   { 'var' : 'el_pt' , 'type': 'float', 'bins': [20,30,40,50,60,100,200,500] },

]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = { 
#    0 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    1 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    2 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    3 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    4 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    5 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    6 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    7 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    8 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    9 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45'
    0 : cutpassMVA94XwpLnoiso,
    1 : cutpassMVA94XwpLnoiso,
    2 : cutpassMVA94XwpLnoiso,
    3 : cutpassMVA94XwpLnoiso,
    4 : cutpassMVA94XwpLnoiso,
    5 : cutpassMVA94XwpLnoiso,
    6 : cutpassMVA94XwpLnoiso,
    7 : cutpassMVA94XwpLnoiso,
    8 : cutpassMVA94XwpLnoiso,
    9 : cutpassMVA94XwpLnoiso,
    10 : cutpassMVA94XwpLnoiso,
    11 : cutpassMVA94XwpLnoiso,
    12 : cutpassMVA94XwpLnoiso,
    13 : cutpassMVA94XwpLnoiso,
    14 : cutpassMVA94XwpLnoiso,
    15 : cutpassMVA94XwpLnoiso,
    16 : cutpassMVA94XwpLnoiso,
    17 : cutpassMVA94XwpLnoiso,
    18 : cutpassMVA94XwpLnoiso,
    19 : cutpassMVA94XwpLnoiso,
    20 : cutpassMVA94XwpLnoiso,
    21 : cutpassMVA94XwpLnoiso,
    22 : cutpassMVA94XwpLnoiso,
    23 : cutpassMVA94XwpLnoiso,
    24 : cutpassMVA94XwpLnoiso,
    25 : cutpassMVA94XwpLnoiso,
    26 : cutpassMVA94XwpLnoiso,
    27 : cutpassMVA94XwpLnoiso,
    28 : cutpassMVA94XwpLnoiso,
    29 : cutpassMVA94XwpLnoiso,
    30 : cutpassMVA94XwpLnoiso,
    31 : cutpassMVA94XwpLnoiso,
    32 : cutpassMVA94XwpLnoiso,
    33 : cutpassMVA94XwpLnoiso,
    34 : cutpassMVA94XwpLnoiso,
#    35 : cutpassMVA94Xwp90noiso,
#    36 : cutpassMVA94Xwp90noiso,
#    37 : cutpassMVA94Xwp90noiso,
#    38 : cutpassMVA94Xwp90noiso,
#    39 : cutpassMVA94Xwp90noiso,
}

#### or remove any additional cut (default)
#additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
    ]

#tnpParAltSigFit = [
#    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
#    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
#    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
#    ]
tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,0.05,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,0.05,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
     
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]
        
