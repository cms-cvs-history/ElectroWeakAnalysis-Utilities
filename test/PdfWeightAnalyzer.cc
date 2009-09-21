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
      std::vector<edm::InputTag> pdfWeightTags_;
      unsigned int originalEvents_;
      std::vector<int> pdfStart_;
      std::vector<double> weightedEvents_;
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
  pdfWeightTags_(pset.getUntrackedParameter<std::vector<edm::InputTag> > ("PdfWeightTags")) { 
}

/////////////////////////////////////////////////////////////////////////////////////
PdfWeightAnalyzer::~PdfWeightAnalyzer(){}

/////////////////////////////////////////////////////////////////////////////////////
void PdfWeightAnalyzer::beginJob(const edm::EventSetup& eventSetup){
      originalEvents_ = 0;
      edm::LogVerbatim("") << "PDF uncertainties will be determined for the following sets: ";
      //weightedEvents_.push_back(std::vector<double>()); 
      for (unsigned int i=0; i<pdfWeightTags_.size(); ++i) {
            edm::LogVerbatim("") << "\t" << pdfWeightTags_[i].instance();
            pdfStart_.push_back(-1);
      }
}

/////////////////////////////////////////////////////////////////////////////////////
void PdfWeightAnalyzer::endJob(){
      edm::LogVerbatim("") << "\n>>>>>> PDF weight systematics summary >>>>";
      edm::LogVerbatim("") << "Analyzed (reference): " << originalEvents_ << " [events]";
      if (originalEvents_==0) return;
      for (unsigned int i=0; i<pdfWeightTags_.size(); ++i) {
            double nmembers = weightedEvents_.size()-pdfStart_[i];
            if (i<pdfWeightTags_.size()-1) nmembers = pdfStart_[i+1] - pdfStart_[i];
            double npairs = (nmembers-1)/2;
            edm::LogVerbatim("") << "\nResults for PDF set " << pdfWeightTags_[i].instance() << ", number of uncorrelated variations used: " << npairs;

            double events_central = weightedEvents_[pdfStart_[i]]; 
            edm::LogVerbatim("") << "\tEstimate for central PDF set: " << std::setprecision(4) << events_central << " [events], change with respect to reference: " << std::setprecision(2) << 100*(events_central/originalEvents_-1.) << " [%]";

            double wplus = 0.;
            double wminus = 0.;
            for (unsigned int j=0; j<npairs; ++j) {
                  double wa = weightedEvents_[pdfStart_[i]+2*j+1]/events_central-1.;
                  double wb = weightedEvents_[pdfStart_[i]+2*j+2]/events_central-1.; 
                  if (wa>wb) {
                        if (wa<0.) wa = 0.;
                        if (wb>0.) wb = 0.;
                        wplus += wa*wa;
                        wminus += wb*wb;
                  } else {
                        if (wb<0.) wb = 0.;
                        if (wa>0.) wa = 0.;
                        wplus += wb*wb;
                        wminus += wa*wa;
                  }
            }
            wplus = sqrt(wplus);
            wminus = sqrt(wminus);
            edm::LogVerbatim("") << "\tRelative uncertainty with respect to central: +" << std::setprecision(2) << 100.*wplus << " / -" << std::setprecision(2) << 100.*wminus << " [%]";
      }

}

/////////////////////////////////////////////////////////////////////////////////////
bool PdfWeightAnalyzer::filter(edm::Event & ev, const edm::EventSetup&){
      originalEvents_++;

      for (unsigned int i=0; i<pdfWeightTags_.size(); ++i) {
            edm::Handle<std::vector<double> > weightHandle;
            ev.getByLabel(pdfWeightTags_[i], weightHandle);
            std::vector<double> weights = (*weightHandle);
            unsigned int nmembers = weights.size();
            // Set up arrays the first time wieghts are read
            if (pdfStart_[i]<0) {
                  pdfStart_[i] = weightedEvents_.size();
                  for (unsigned int j=0; j<nmembers; ++j) {
                        weightedEvents_.push_back(0.);
                  }
            }
            
            for (unsigned int j=0; j<nmembers; ++j) {
                  weightedEvents_[pdfStart_[i]+j] += weights[j];
            }

            /*
            printf("\n>>>>>>>>> Run %8d Event %d, members %3d PDF set %s : Weights >>>> \n", ev.id().run(), ev.id().event(), nmembers, pdfWeightTags_[i].instance().data());
            for (unsigned int i=0; i<nmembers; i+=5) {
                  for (unsigned int j=0; ((j<5)&&(i+j<nmembers)); ++j) {
                        printf(" %2d: %7.4f", i+j, weights[i+j]);
                  }
                  safe_printf("\n");
            }
            */

      }

      return true;
}

DEFINE_FWK_MODULE(PdfWeightAnalyzer);
