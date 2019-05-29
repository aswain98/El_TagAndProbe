#include "RooDataHist.h"
#include "RooWorkspace.h"
#include "RooRealVar.h"
#include "RooAbsPdf.h"
#include "RooPlot.h"
#include "RooFitResult.h"
#include "RooChi2Var.h"
#include "RooHist.h"
#include "RooCurve.h"
#include "TH1.h"
#include "TSystem.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TPaveText.h"
#include "TVirtualFitter.h"

/// include pdfs
#include "RooCBExGaussShape.h"
#include "RooCMSShape.h"

#include <vector>
#include <string>
#include <iostream>
#ifdef __CINT__
#pragma link C++ class std::vector<std::string>+;
#endif

using namespace RooFit;
using namespace std;

class tnpFitter {
public:
  tnpFitter( TFile *file, std::string histname  );
  tnpFitter( TH1 *hPass, TH1 *hFail, std::string histname  );
  ~tnpFitter(void) {if( _work != 0 ) delete _work; }
  void setZLineShapes(TH1 *hZPass, TH1 *hZFail );
  void setWorkspace(std::vector<std::string>);
  void setOutputFile(TFile *fOut ) {_fOut = fOut;}
  void fits(bool mcTruth,std::string title = "");
  void useMinos(bool minos = true) {_useMinos = minos;}
  void textParForCanvas(RooFitResult *resP, RooFitResult *resF, TPad *p, double chi2_pass, double chi2_fail);
  
  void fixSigmaFtoSigmaP(bool fix=true) { _fixSigmaFtoSigmaP= fix;}

  void setFitRange(double xMin,double xMax) { _xFitMin = xMin; _xFitMax = xMax; }
private:
  RooWorkspace *_work;
  RooDataHist *_rooHistFail, *_rooHistPass;
  std::string _histname_base;
  TFile *_fOut;
  double _nTotP, _nTotF;
  bool _useMinos;
  bool _fixSigmaFtoSigmaP;
  double _xFitMin,_xFitMax;
  int nParP, nParF;
  double chi2_pass, chi2_fail; 
};

tnpFitter::tnpFitter(TFile *filein, std::string histname   ) : _useMinos(false),_fixSigmaFtoSigmaP(false) {
  //RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);
  //RooMsgService::instance().setStreamStatus(1,false);
  //MinimizerOptions::instance().setDefaultMaxFunctionCalls(1000);
  _histname_base = histname;  

  TH1 *hPass = (TH1*) filein->Get(TString::Format("%s_Pass",histname.c_str()).Data());
  TH1 *hFail = (TH1*) filein->Get(TString::Format("%s_Fail",histname.c_str()).Data());
  _nTotP = hPass->Integral();
  _nTotF = hFail->Integral();
  /// MC histos are done between 50-130 to do the convolution properly
  /// but when doing MC fit in 60-120, need to zero bins outside the range
  for( int ib = 0; ib <= hPass->GetXaxis()->GetNbins()+1; ib++ )
   if(  hPass->GetXaxis()->GetBinCenter(ib) <= 60 || hPass->GetXaxis()->GetBinCenter(ib) >= 120 ) {
     hPass->SetBinContent(ib,0);
     hFail->SetBinContent(ib,0);
   }
  
  _work = new RooWorkspace("w") ;
  _work->factory("x[60,120]");

  RooDataHist rooPass("hPass","hPass",*_work->var("x"),hPass);
  RooDataHist rooFail("hFail","hFail",*_work->var("x"),hFail);
  _rooHistPass = (RooDataHist*) rooPass.Clone();
  _rooHistFail = (RooDataHist*) rooFail.Clone();
  _work->import(rooPass) ;
  _work->import(rooFail) ;
  _xFitMin = 60;
  _xFitMax = 120;
}

tnpFitter::tnpFitter(TH1 *hPass, TH1 *hFail, std::string histname  ) : _useMinos(false),_fixSigmaFtoSigmaP(false) {
  //RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);
  //RooMsgService::instance().setStreamStatus(1,false);
  //MinimizerOptions::instance().setDefaultMaxFunctionCalls(1000);
  _histname_base = histname;
  
  _nTotP = hPass->Integral();
  _nTotF = hFail->Integral();
  /// MC histos are done between 50-130 to do the convolution properly
  /// but when doing MC fit in 60-120, need to zero bins outside the range
  for( int ib = 0; ib <= hPass->GetXaxis()->GetNbins()+1; ib++ )
    if(  hPass->GetXaxis()->GetBinCenter(ib) <= 60 || hPass->GetXaxis()->GetBinCenter(ib) >= 120 ) {
      hPass->SetBinContent(ib,0);
      hFail->SetBinContent(ib,0);
    }
  
  _work = new RooWorkspace("w") ;
  _work->factory("x[60,120]");
  
  RooDataHist rooPass("hPass","hPass",*_work->var("x"),hPass);
  RooDataHist rooFail("hFail","hFail",*_work->var("x"),hFail);
  _rooHistPass = (RooDataHist*) rooPass.Clone();
  _rooHistFail = (RooDataHist*) rooFail.Clone();
  _work->import(rooPass) ;
  _work->import(rooFail) ;
  _xFitMin = 60;
  _xFitMax = 120;
  
}


void tnpFitter::setZLineShapes(TH1 *hZPass, TH1 *hZFail ) {
  RooDataHist rooPass("hGenZPass","hGenZPass",*_work->var("x"),hZPass);
  RooDataHist rooFail("hGenZFail","hGenZFail",*_work->var("x"),hZFail);
  _work->import(rooPass) ;
  _work->import(rooFail) ;  
}

void tnpFitter::setWorkspace(std::vector<std::string> workspace) {
  for( unsigned icom = 0 ; icom < workspace.size(); ++icom ) {
    _work->factory(workspace[icom].c_str());
  }

  _work->factory("HistPdf::sigPhysPass(x,hGenZPass)");
  _work->factory("HistPdf::sigPhysFail(x,hGenZFail)");
  _work->factory("FCONV::sigPass(x, sigPhysPass , sigResPass)");
  _work->factory("FCONV::sigFail(x, sigPhysFail , sigResFail)");
  _work->factory(TString::Format("nSigP[%f,0.5,%f]",_nTotP*0.9,_nTotP*1.5));
  _work->factory(TString::Format("nBkgP[%f,0.5,%f]",_nTotP*0.1,_nTotP*1.5));
  _work->factory(TString::Format("nSigF[%f,0.5,%f]",_nTotF*0.9,_nTotF*1.5));
  _work->factory(TString::Format("nBkgF[%f,0.5,%f]",_nTotF*0.1,_nTotF*1.5));
  _work->factory("SUM::pdfPass(nSigP*sigPass,nBkgP*bkgPass)");
  _work->factory("SUM::pdfFail(nSigF*sigFail,nBkgF*bkgFail)");
  _work->Print();			         
}

void tnpFitter::fits(bool mcTruth,string title) {
  TVirtualFitter::SetMaxIterations(10000);
  std::ostream & os = std::cout;

  cout << " title : " << title << endl;

  
  RooAbsPdf *pdfPass = _work->pdf("pdfPass");
  RooAbsPdf *pdfFail = _work->pdf("pdfFail");

  if( mcTruth ) {
    _work->var("nBkgP")->setVal(0); _work->var("nBkgP")->setConstant();
    _work->var("nBkgF")->setVal(0); _work->var("nBkgF")->setConstant();
    if( _work->var("sosP")   ) { _work->var("sosP")->setVal(0);
      _work->var("sosP")->setConstant(); }
    if( _work->var("sosF")   ) { _work->var("sosF")->setVal(0);
      _work->var("sosF")->setConstant(); }
    if( _work->var("acmsP")  ) _work->var("acmsP")->setConstant();
    if( _work->var("acmsF")  ) _work->var("acmsF")->setConstant();
    if( _work->var("betaP")  ) _work->var("betaP")->setConstant();
    if( _work->var("betaF")  ) _work->var("betaF")->setConstant();
    if( _work->var("gammaP") ) _work->var("gammaP")->setConstant();
    if( _work->var("gammaF") ) _work->var("gammaF")->setConstant();
  }

  /// FC: seems to be better to change the actual range than using a fitRange in the fit itself (???)
  /// FC: I don't know why but the integral is done over the full range in the fit not on the reduced range
  _work->var("x")->setRange(_xFitMin,_xFitMax);
  _work->var("x")->setRange("fitMassRange",_xFitMin,_xFitMax);
  //if (_useMinos) {cout<< "Using Minos"<<endl;}
  //else {cout<< "_useMinos = False "<<endl;}

  RooFitResult* resPass = pdfPass->fitTo(*_work->data("hPass"),Minos(_useMinos),SumW2Error(kTRUE),Save(),Range("fitMassRange"));
  //RooFitResult* resPass = pdfPass->fitTo(*_work->data("hPass"),Minos(_useMinos),SumW2Error(kTRUE),Save());
  if( _fixSigmaFtoSigmaP ) {
    _work->var("sigmaF")->setVal( _work->var("sigmaP")->getVal() );
    _work->var("sigmaF")->setConstant();
  }
  //cout<<"Fit pass with Status == "<< resPass->status() <<endl;
  //resPass->printValue(std::cout);
  _work->var("sigmaF")->setVal(_work->var("sigmaP")->getVal());
  _work->var("sigmaF")->setRange(0.8* _work->var("sigmaP")->getVal(), 3.0* _work->var("sigmaP")->getVal());
  RooFitResult* resFail = pdfFail->fitTo(*_work->data("hFail"),Minos(_useMinos),SumW2Error(kTRUE),Save(),Range("fitMassRange"));
  //RooFitResult* resFail = pdfFail->fitTo(*_work->data("hFail"),Minos(_useMinos),SumW2Error(kTRUE),Save());
  //cout<<"Fit fail with Status == "<< resFail->status() <<endl;
  //resFail->printValue(std::cout);

  RooPlot *pPass = _work->var("x")->frame(60,120);
  RooPlot *pFail = _work->var("x")->frame(60,120);
  //RooPlot *pChkPass = _work->var("x")->frame(60,120);
  //RooPlot *pChkFail = _work->var("x")->frame(60,120);
  pPass->SetTitle("passing probe");
  pFail->SetTitle("failing probe");
  
  _work->data("hPass") ->plotOn( pPass, Name("h_hPass") );
  _work->pdf("pdfPass")->plotOn( pPass, Name("PDFmodelP"), LineColor(kRed) );
  _work->pdf("pdfPass")->plotOn( pPass, Components("bkgPass"),LineColor(kBlue),LineStyle(kDashed));
  _work->data("hPass") ->plotOn( pPass, Name("hPass") );
  
  _work->data("hFail") ->plotOn( pFail, Name("h_hFail"));
  _work->pdf("pdfFail")->plotOn( pFail, Name("PDFmodelF"), LineColor(kRed) );
  _work->pdf("pdfFail")->plotOn( pFail, Components("bkgFail"),LineColor(kBlue),LineStyle(kDashed));
  _work->data("hFail") ->plotOn( pFail, Name("hFail") );

  double x,y;
  
  TCanvas c1("c1","c1",1100,450);
  //_work->data("hPass") ->plotOn( pChkPass, Name("h_hPass"));
  nParP = 0;
  nParP = resPass->floatParsFinal().getSize();
  cout << "nPar = "<< resPass->floatParsFinal().getSize() <<endl;
  chi2_pass = 0;
  RooCurve* curveP = (RooCurve*) pPass->findObject("PDFmodelP",RooCurve::Class());
  RooHist* histP = (RooHist*) pPass->findObject("h_hPass",RooHist::Class());
  int nEntriesP = 0;
  int i,nBinsP = histP->GetN();
  if (nBinsP != 60) cout<<"nBins of histP not matching expected value"<<endl;
  for (int bin=0; bin < nBinsP; bin++){
    histP->GetPoint(bin,x,y);
    if(y!=0) nEntriesP ++;
  }
  pPass->Draw();
  chi2_pass = pPass->chiSquare("PDFmodelP", "h_hPass", 0);
  cout<< "raw Chi2 = " << chi2_pass*nEntriesP <<endl;
  chi2_pass = chi2_pass*nEntriesP/(nBinsP-nParP);
  cout<< "manually reduced chi2 = "<<chi2_pass<<endl;
  RooHist* ResHistP = histP->makeResidHist(*curveP, true, false);
  RooPlot* ResHistPass = _work->var("x")->frame(60,120);
  ResHistPass->SetTitle("PullHist (passing)");
  ResHistPass->addPlotable(ResHistP,"P");


  TCanvas c2("c2","c2",1100,450);
  //pFail->Print("v");
  nParF = 0;
  nParF = resFail->floatParsFinal().getSize();
  cout<< "nPar = "<< resFail->floatParsFinal().getSize()<<endl;
  chi2_fail = 0;
  RooCurve* curveF = (RooCurve*) pFail->findObject("PDFmodelF",RooCurve::Class());
  RooHist* histF = (RooHist*) pFail->findObject("h_hFail",RooHist::Class());
  int nEntriesF = 0;
  int j,nBinsF = histF->GetN();
  if (nBinsF != 60) cout<<"nBins of histF not matching expected value"<<endl;
  for (int bin=0; bin < nBinsF; bin++){
    histF->GetPoint(bin,x,y);
    if(y!=0) nEntriesF ++;
  } 
  pFail->Draw();
  chi2_fail = pFail->chiSquare("PDFmodelF", "h_hFail", 0);
  cout<< "raw Chi2 = " << chi2_fail*nEntriesF <<endl;
  chi2_fail = chi2_fail*nEntriesF/(nBinsF-nParF);
  cout<< "manually reduced chi2 = "<<chi2_fail<<endl;
  RooHist* ResHistF = histF->makeResidHist(*curveF, true, false);
  RooPlot* ResHistFail = _work->var("x")->frame(60,120);
  ResHistFail->SetTitle("PullHist (failing)");
  ResHistFail->addPlotable(ResHistF,"P");

  TCanvas c("c","c",1100,600);
  c.Divide(3,1);
  TPad *padText = (TPad*)c.GetPad(1);
  textParForCanvas( resPass,resFail, padText, chi2_pass, chi2_fail);
  c.cd(2); gPad->Divide(1,2); gPad->cd(1); pPass->Draw();
  c.cd(2); gPad->cd(2);ResHistPass->Draw();
  c.cd(3); gPad->Divide(1,2); gPad->cd(1); pFail->Draw();
  c.cd(3); gPad->cd(2); ResHistFail->Draw();
  //c.cd(5); ResHistPass->Draw();
  //c.cd(6); ResHistFail->Draw();
  
  _fOut->cd();
  c.Write(TString::Format("%s_Canv",_histname_base.c_str()),TObject::kOverwrite);
  resPass->Write(TString::Format("%s_resP",_histname_base.c_str()),TObject::kOverwrite);
  resFail->Write(TString::Format("%s_resF",_histname_base.c_str()),TObject::kOverwrite);

  
}





/////// Stupid parameter dumper /////////
void tnpFitter::textParForCanvas(RooFitResult *resP, RooFitResult *resF,TPad *p, double chi2_pass, double chi2_fail) {

  double eff = -1;
  double e_eff = 0;

  RooRealVar *nSigP = _work->var("nSigP");
  RooRealVar *nSigF = _work->var("nSigF");
  
  double nP   = nSigP->getVal();
  double e_nP = nSigP->getError();
  double nF   = nSigF->getVal();
  double e_nF = nSigF->getError();
  double nTot = nP+nF;
  eff = nP / (nP+nF);
  e_eff = 1./(nTot*nTot) * sqrt( nP*nP* e_nF*e_nF + nF*nF * e_nP*e_nP );

  TPaveText *text1 = new TPaveText(0,0.8,1,1);
  text1->SetFillColor(0);
  text1->SetBorderSize(0);
  text1->SetTextAlign(12);

  text1->AddText(TString::Format("* fit status pass: %d, fail : %d",resP->status(),resF->status()));
  text1->AddText(TString::Format("* chi2/nDoF pass: %f, fail : %f", chi2_pass, chi2_fail));
  text1->AddText(TString::Format("* minNll pass: %f, fail : %f", resP->minNll(), resF->minNll()));
  text1->AddText(TString::Format("* eff = %1.4f #pm %1.4f",eff,e_eff));

  //  text->SetTextSize(0.06);

//  text->AddText("* Passing parameters");
  TPaveText *text = new TPaveText(0,0,1,0.8);
  text->SetFillColor(0);
  text->SetBorderSize(0);
  text->SetTextAlign(12);
  text->AddText("    --- parmeters " );
  RooArgList listParFinalP = resP->floatParsFinal();
  for( int ip = 0; ip < listParFinalP.getSize(); ip++ ) {
    TString vName = listParFinalP[ip].GetName();
    text->AddText(TString::Format("   - %s \t= %1.3f #pm %1.3f",
				  vName.Data(),
				  _work->var(vName)->getVal(),
				  _work->var(vName)->getError() ) );
  }

//  text->AddText("* Failing parameters");
  RooArgList listParFinalF = resF->floatParsFinal();
  for( int ip = 0; ip < listParFinalF.getSize(); ip++ ) {
    TString vName = listParFinalF[ip].GetName();
    text->AddText(TString::Format("   - %s \t= %1.3f #pm %1.3f",
				  vName.Data(),
				  _work->var(vName)->getVal(),
				  _work->var(vName)->getError() ) );
  }

  p->cd();
  text1->Draw();
  text->Draw();
}
