////////// Header section /////////////////////////////////////////////
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

class FSRWeightAnalyzer: public edm::EDFilter {
public:
      FSRWeightAnalyzer(const edm::ParameterSet& pset);
      virtual ~FSRWeightAnalyzer();
      virtual bool filter(edm::Event &, const edm::EventSetup&);
      virtual void beginJob(const edm::EventSetup& eventSetup) ;
      virtual void endJob() ;
private:
      edm::InputTag weightTag_;
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
FSRWeightAnalyzer::FSRWeightAnalyzer(const edm::ParameterSet& pset) :
  weightTag_(pset.getUntrackedParameter<edm::InputTag> ("WeightTag", edm::InputTag("fsrWeight"))) { 
}

/////////////////////////////////////////////////////////////////////////////////////
FSRWeightAnalyzer::~FSRWeightAnalyzer(){}

/////////////////////////////////////////////////////////////////////////////////////
void FSRWeightAnalyzer::beginJob(const edm::EventSetup& eventSetup){}

/////////////////////////////////////////////////////////////////////////////////////
void FSRWeightAnalyzer::endJob(){}

/////////////////////////////////////////////////////////////////////////////////////
bool FSRWeightAnalyzer::filter(edm::Event & ev, const edm::EventSetup&){
      edm::Handle<double> weightHandle;
      ev.getByLabel(weightTag_, weightHandle);
      double weight = *weightHandle;

      safe_printf("\n>>>>>>>>> Run %8d Event %d, Event weight for ISR systematics = 1 + %e\n", ev.id().run(), ev.id().event(), weight-1);

      return true;
}

/////////////////////////////////////////////////////////////////////////////////////
#include <stdarg.h>
void FSRWeightAnalyzer::safe_printf(const char* fmt, ...) {
      const unsigned int bufsize = 256;
      char chout[bufsize];
      va_list variables;
      va_start(variables, fmt);
      vsnprintf(chout, bufsize, fmt, variables);
      std::cout << chout;
      va_end(variables);
}

DEFINE_FWK_MODULE(FSRWeightAnalyzer);
