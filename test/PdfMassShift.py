import FWCore.ParameterSet.Config as cms

# Process name
process = cms.Process("PDFANA")

# Max events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    #input = cms.untracked.int32(10)
)

# Printouts
process.MessageLogger = cms.Service("MessageLogger",
      cout = cms.untracked.PSet(
            default = cms.untracked.PSet(limit = cms.untracked.int32(100)),
            threshold = cms.untracked.string('INFO')
      ),
      destinations = cms.untracked.vstring('cout')
)

# Input files (on disk)
process.source = cms.Source("PoolSource",
      fileNames = cms.untracked.vstring("file:/data4/ZMuMu_Summer09-MC_31X_V3_preproduction_312-v1_RECO/20A5B350-6979-DE11-A6EF-001560AD3140.root")
)

# Produce PDF weights (maximum is 3)
process.pdfWeights = cms.EDProducer("PdfWeightProducer",
      PdfInfoTag = cms.untracked.InputTag("generator"),
      PdfSetNames = cms.untracked.vstring(
              "cteq65.LHgrid"
            #, "MRST2006nnlo.LHgrid"
            #, "MRST2007lomod.LHgrid"
      )
)

# Collect uncertainties for rate and acceptance
process.pdfSystematics = cms.EDFilter("PdfMassShift",
      SelectorPath = cms.untracked.string('pdfana'),
      GenParticlesTag = cms.untracked.InputTag("genParticles"),
      PdfWeightTags = cms.untracked.VInputTag(
              "pdfWeights:cteq65"
            #, "pdfWeights:MRST2006nnlo"
            #, "pdfWeights:MRST2007lomod"
      )
)

process.load("ElectroWeakAnalysis/Utilities/zmmSelection_cfi")

# Main path
process.pdfana = cms.Path(
       process.pdfWeights
      *process.goldenZMMSelectionSequence
)

process.end = cms.EndPath(process.pdfSystematics)
