import FWCore.ParameterSet.Config as cms

# Process name
process = cms.Process("WFSRAna")

# Max events
process.maxEvents = cms.untracked.PSet(
    #input = cms.untracked.int32(-1)
    input = cms.untracked.int32(100)
)

# Printouts
process.MessageLogger = cms.Service("MessageLogger",
      debugModules = cms.untracked.vstring('WFSRWeight','weightAnalyzer'),
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

# Produce event weights according to FSR QED O(alpha) matrix element + missing NLO
process.WFSRWeight = cms.EDProducer("WFSRWeightProducer",
      GenTag = cms.untracked.InputTag("generator"),
)

# Check that it is fine
process.weightAnalyzer = cms.EDFilter("WFSRWeightAnalyzer",
      WeightTag = cms.untracked.InputTag("WFSRWeight")
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
      cms.untracked.vstring('keep *_WFSRWeight_*_*')
)

# Output (optionaly filtered by path)
process.output = cms.OutputModule("PoolOutputModule",
    process.MyEventContent,
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('WFSRAna')
    ),
    fileName = cms.untracked.string('WFSRWeighted_Events.root')
)

# Runnning and end paths
process.WFSRAna = cms.Path(process.WFSRWeight*process.weightAnalyzer*process.printGenParticles)
process.end = cms.EndPath(process.output)
