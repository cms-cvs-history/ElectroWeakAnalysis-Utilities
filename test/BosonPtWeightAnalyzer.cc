////////// Header section /////////////////////////////////////////////
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

class BosonPtWeightAnalyzer: public edm::EDFilter {
public:
      BosonPtWeightAnalyzer(const edm::ParameterSet& pset);
      virtual ~BosonPtWeightAnalyzer();
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
BosonPtWeightAnalyzer::BosonPtWeightAnalyzer(const edm::ParameterSet& pset) :
  weightTag_(pset.getUntrackedParameter<edm::InputTag> ("WeightTag", edm::InputTag("bosonPtWeight"))) { 
}

/////////////////////////////////////////////////////////////////////////////////////
BosonPtWeightAnalyzer::~BosonPtWeightAnalyzer(){}

/////////////////////////////////////////////////////////////////////////////////////
void BosonPtWeightAnalyzer::beginJob(const edm::EventSetup& eventSetup){}

/////////////////////////////////////////////////////////////////////////////////////
void BosonPtWeightAnalyzer::endJob(){}

/////////////////////////////////////////////////////////////////////////////////////
bool BosonPtWeightAnalyzer::filter(edm::Event & ev, const edm::EventSetup&){
      edm::Handle<double> weightHandle;
      ev.getByLabel(weightTag_, weightHandle);
      double weight = *weightHandle;

      safe_printf("\n>>>>>>>>> Run %8d Event %d, Event weight for boson Pt systematics = %7.4f\n", ev.id().run(), ev.id().event(), weight);

      return true;
}

/////////////////////////////////////////////////////////////////////////////////////
#include <stdarg.h>
void BosonPtWeightAnalyzer::safe_printf(const char* fmt, ...) {
      const unsigned int bufsize = 256;
      char chout[bufsize];
      va_list variables;
      va_start(variables, fmt);
      vsnprintf(chout, bufsize, fmt, variables);
      std::cout << chout;
      va_end(variables);
}

DEFINE_FWK_MODULE(BosonPtWeightAnalyzer);
