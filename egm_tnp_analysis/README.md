Note: these are run on lxplus

## Set-up egm_tnp_analysis
~~~~
source etc/scripts/setup94.sh
make
export PYTHONPATH=$PYTHONPATH:/afs/cern.ch/user/<u>/<username>/work/TagAndProbe/CMSSW_9_4_0/src/egm_tnp_analysis
~~~~

## Get PU reweight
~~~~
nohup python etc/scripts/pureweight.py > pureweight.log 2>&1 &
~~~~

## Update config files (etc/config/setting_ele_iso.py)
- include custom WP : 'passingMini==1' 
- update MVA WP to V2 :'passingMVA94Xwp90noisoV2 == 1'
- add in additional cuts to require passing denominator ID
- update putree file path (search for set_puTree[''])
- update baseOutDir (This is a relative path. Used in tnpEGM_fitter.py {outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,args.flag)}. The corresponding directory will be created when running --createBins option and plots from --doFit / --sumUp will be stored inside.)

## Update file paths of input sample (etc/inputs/tnpSampleDef.py)

## Run fitting script
~~~~
python tnpEGM_fitter.py etc/config/settings_ele_iso.py --flag passingMiniIsoTight --checkBins
python tnpEGM_fitter.py etc/config/settings_ele_iso.py --flag passingMiniIsoTight --createBins
nohup python tnpEGM_fitter.py etc/config/settings_ele_iso.py --flag passingMiniIsoTight --createHists > createHists_refit.log 2>&1 &
nohup python tnpEGM_fitter.py etc/config/settings_ele_iso.py --flag passingMiniIsoTight --doFit > dofit_refit.log 2>&1 &
nohup python tnpEGM_fitter.py etc/config/settings_ele_iso.py --flag passingMiniIsoTight --doFit --mcSig --altSig  > mcSig_refit.log 2>&1 &
nohup python tnpEGM_fitter.py etc/config/settings_ele_iso.py --flag passingMiniIsoTight --doFit --altSig > altSig_refit.log 2>&1 &
nohup python tnpEGM_fitter.py etc/config/settings_ele_iso.py --flag passingMiniIsoTight --doFit --altBkg > altBkg_refit.log 2>&1 &
nohup python tnpEGM_fitter.py etc/config/settings_ele_iso.py --flag passingMiniIsoTight --sumUp > sumUp.log 2>&1 &
~~~~
