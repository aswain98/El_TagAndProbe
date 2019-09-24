from libPython.tnpClassUtils import tnpSample

### qll stat
#eosDir1 = 'eos/cms/store/group/phys_egamma/tnp/80X/PhoEleIDs/v1/'
#eosDir2 = 'eos/cms/store/group/phys_egamma/tnp/80X/PhoEleIDs/v2/'
#eosDirREC = 'eos/cms/store/group/phys_egamma/tnp/80X/RecoSF/RECOSFs_2016/'
#eosWinter17 = 'eos/cms/store/group/phys_egamma/tnp/80X/PhoEleIDs/Moriond17_v1/'
workaswain = '/afs/cern.ch/work/a/aswain/'

Moriond18_94X = {
    ### MiniAOD TnP for IDs scale factors
    'DY_madgraph'          : tnpSample('DY_madgraph',
                                       workaswain + 'finalone.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_madgraph_Moriond18' : tnpSample('DY_madgraph_Moriond18', 
                                       workaswain + 'finalone.root',
                                       isMC = True, nEvts =  -1 ),
    #'DY_amcatnlo_Moriond18' : tnpSample('DY_amcatnlo_Moriond18', 
    #                                  workaswain + 'mc/TnPTree_DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_all.root',
    #                                   isMC = True, nEvts =  -1 ),

    'data_Run2017B' : tnpSample('data_Run2017B' , workaswain + 'eleTnPTree/TnPTree_31Mar18_RunB_hadd.root' , lumi = 4.891 ),
    'data_Run2017C' : tnpSample('data_Run2017C' , workaswain + 'eleTnPTree/TnPTree_31Mar18_RunC_hadd.root' , lumi = 9.9 ),
    'data_Run2017D' : tnpSample('data_Run2017D' , workaswain + 'eleTnPTree/TnPTree_31Mar18_RunD_hadd.root' , lumi = 4.36 ),
    'data_Run2017E' : tnpSample('data_Run2017E' , workaswain + 'eleTnPTree/TnPTree_31Mar18_RunE_hadd.root' , lumi = 9.53 ),
    'data_Run2017F' : tnpSample('data_Run2017F' , workaswain + 'eleTnPTree/TnPTree_31Mar18_RunF_hadd.root' , lumi = 13.96 ),

    }
