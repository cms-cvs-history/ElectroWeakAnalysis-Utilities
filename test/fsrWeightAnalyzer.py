import FWCore.ParameterSet.Config as cms

# Process name
process = cms.Process("fsrAna")

# Max events
process.maxEvents = cms.untracked.PSet(
    #input = cms.untracked.int32(-1)
    input = cms.untracked.int32(100)
)

# Printouts
process.MessageLogger = cms.Service("MessageLogger",
      debugModules = cms.untracked.vstring('fsrWeight','weightAnalyzer'),
      cout = cms.untracked.PSet(
            #default = cms.untracked.PSet(
            #      limit = cms.untracked.int32(10)
            #),
            threshold = cms.untracked.string('INFO')
      ),
      destinations = cms.untracked.vstring('cout')
)

# Input files (on disk)
process.source = cms.Source("PoolSource",
      debugVerbosity = cms.untracked.uint32(0),
      debugFlag = cms.untracked.bool(False),
      fileNames = cms.untracked.vstring("file:/data4/Wmunu-Summer09-MC_31X_V2_preproduction_311-v1/0011/F4C91F77-766D-DE11-981F-00163E1124E7.root")
      #fileNames = cms.untracked.vstring("file:/dataamscie1b/Wmunu-Summer09-MC_31X_V2_preproduction_311-v1/0011/F4C91F77-766D-DE11-981F-00163E1124E7.root")
)

# Produce event weights according to generated boson Pt
# Example corresponds to approximate weights to study
# systematic effects due to ISR uncertainties (Z boson)
process.fsrWeight = cms.EDProducer("FSRWeightProducer",
      GenTag = cms.untracked.InputTag("generator"),
)

# Check that it is fine
process.weightAnalyzer = cms.EDFilter("FSRWeightAnalyzer",
      WeightTag = cms.untracked.InputTag("fsrWeight")
)

process.include("SimGeneral/HepPDTESSource/data/pythiapdt.cfi")
process.printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
  maxEventsToPrint = cms.untracked.int32(1),
  printVertex = cms.untracked.bool(False),
  src = cms.InputTag("genParticles")
)

# Save weights in the output file 
process.load("Configuration.EventContent.EventContent_cff")
process.MyEventContent = cms.PSet( 
      outputCommands = process.AODSIMEventContent.outputCommands
)
process.MyEventContent.outputCommands.extend(
      cms.untracked.vstring('keep *_fsrWeight_*_*')
)

# Output (optionaly filtered by path)
process.output = cms.OutputModule("PoolOutputModule",
    process.MyEventContent,
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('fsrAna')
    ),
    fileName = cms.untracked.string('fsrWeighted_Events.root')
)

# Runnning and end paths
process.fsrAna = cms.Path(process.fsrWeight*process.weightAnalyzer*process.printGenParticles)
process.end = cms.EndPath(process.output)
