#export  PYTHONPATH=$PYTHONPATH:/afs/cern.ch/user/s/soffi/scratch0/TEST/CMSSW-10-0-0-pre3/src/egm_tnp_analysis
import etc.inputs.tnpSampleDef as tnpSamples
from libPython.tnpClassUtils import mkdir
import libPython.puReweighter as pu
import os
puType = 0

for sName in tnpSamples.Moriond18_94X.keys():  
    print sName  
    sample = tnpSamples.Moriond18_94X[sName]
    if sample is None : continue
#    if not 'rec' in sName : continue
#    if not 'Winter17' in sName : continue
#    if not 'DY' in sName: continue
    if not 'madgraph' in sName: continue
    if not sample.isMC: continue
    
    trees = {}
    trees['ele'] = 'tnpEleIDs'
#    trees['pho'] = 'tnpPhoIDs'
#    trees['rec'] = 'GsfElectronToSC'
    for tree in trees:
        dirout =  '/afs/cern.ch/user/w/wiwong/work/TagAndProbe/CMSSW_9_4_0/src/egm_tnp_analysis/PUTree/'
        if not os.path.exists(dirout):
          mkdir(dirout)
        
        if   puType == 0 : sample.set_puTree( dirout + '%s_%s.pu.puTree.root'   % (sample.name,tree) )
        elif puType == 1 : sample.set_puTree( dirout + '%s_%s.nVtx.puTree.root' % (sample.name,tree) )
        elif puType == 2 : sample.set_puTree( dirout + '%s_%s.rho.puTree.root'  % (sample.name,tree) )
        sample.set_tnpTree(trees[tree]+'/fitter_tree')
        sample.dump()
        pu.reweight(sample, puType )
    
