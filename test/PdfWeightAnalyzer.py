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
      debugModules = cms.untracked.vstring('pdfWeights','pdfAnalyzer'),
      cout = cms.untracked.PSet(
            default = cms.untracked.PSet(
                  limit = cms.untracked.int32(10)
            ),
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

# Produce PDF weights (maximum is 3)
process.pdfWeights = cms.EDProducer("PdfWeightProducer",
      PdfInfoTag = cms.untracked.InputTag("generator"),
      PdfSetNames = cms.untracked.vstring(
              "cteq65.LHgrid"
            , "MRST2006nnlo.LHgrid"
            , "MRST2007lomod.LHgrid"
      )
)

# Check that it is fine
process.pdfAnalyzer = cms.EDFilter("PdfWeightAnalyzer",
      PdfWeightTags = cms.untracked.VInputTag(
              "pdfWeights:cteq65"
            , "pdfWeights:MRST2006nnlo"
            , "pdfWeights:MRST2007lomod"
      )
)

# Save PDF weights in the output file 
process.load("Configuration.EventContent.EventContent_cff")
process.MyEventContent = cms.PSet( 
      outputCommands = process.AODSIMEventContent.outputCommands
)
process.MyEventContent.outputCommands.extend(
      cms.untracked.vstring('keep *_pdfWeights_*_*')
)

# Output (optionaly filtered by path)
process.pdfOutput = cms.OutputModule("PoolOutputModule",
    process.MyEventContent,
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('pdfana')
    ),
    fileName = cms.untracked.string('pdfAnalyzer_Events.root')
)

# Runnning and end paths
process.pdfana = cms.Path(process.pdfWeights*process.pdfAnalyzer)
process.end = cms.EndPath(process.pdfOutput)
