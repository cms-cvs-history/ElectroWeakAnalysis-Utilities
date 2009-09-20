////////// Header section /////////////////////////////////////////////
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

class PdfWeightAnalyzer: public edm::EDFilter {
public:
      PdfWeightAnalyzer(const edm::ParameterSet& pset);
      virtual ~PdfWeightAnalyzer();
      virtual bool filter(edm::Event &, const edm::EventSetup&);
      virtual void beginJob(const edm::EventSetup& eventSetup) ;
      virtual void endJob() ;
private:
      edm::InputTag pdfWeightTag_;
      void safe_printf(const char* fmt, ...);
};

////////// Source code ////////////////////////////////////////////////
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/Common/interface/Handle.h"

/////////////////////////////////////////////////////////////////////////////////////
PdfWeightAnalyzer::PdfWeightAnalyzer(const edm::ParameterSet& pset) :
  pdfWeightTag_(pset.getUntrackedParameter<edm::InputTag> ("PdfWeightTag")) { 
}

/////////////////////////////////////////////////////////////////////////////////////
PdfWeightAnalyzer::~PdfWeightAnalyzer(){}

/////////////////////////////////////////////////////////////////////////////////////
void PdfWeightAnalyzer::beginJob(const edm::EventSetup& eventSetup){}

/////////////////////////////////////////////////////////////////////////////////////
void PdfWeightAnalyzer::endJob(){}

/////////////////////////////////////////////////////////////////////////////////////
bool PdfWeightAnalyzer::filter(edm::Event & ev, const edm::EventSetup&){
      edm::Handle<std::vector<double> > weightHandle;
      ev.getByLabel(pdfWeightTag_, weightHandle);
      std::vector<double> weights = (*weightHandle);
      unsigned int nmembers = weights.size();

      safe_printf("\n>>>>>>>>> Run %8d Event %d, members %3d PDF set member: Weights >>>> \n", ev.id().run(), ev.id().event(), nmembers);
      for (unsigned int i=0; i<nmembers; i+=5) {
        for (unsigned int j=0; ((j<5)&&(i+j<nmembers)); ++j) {
            safe_printf(" %2d: %7.4f", i+j, weights[i+j]);
        }
        safe_printf("\n");
      }

      return true;
}

/////////////////////////////////////////////////////////////////////////////////////
#include <stdarg.h>
void PdfWeightAnalyzer::safe_printf(const char* fmt, ...) {
      const unsigned int bufsize = 256;
      char chout[bufsize];
      va_list variables;
      va_start(variables, fmt);
      vsnprintf(chout, bufsize, fmt, variables);
      std::cout << chout;
      va_end(variables);
}

DEFINE_FWK_MODULE(PdfWeightAnalyzer);
