import FWCore.ParameterSet.Config as cms

# Process name
process = cms.Process("BosonPtAna")

# Max events
process.maxEvents = cms.untracked.PSet(
    #input = cms.untracked.int32(-1)
    input = cms.untracked.int32(10)
)

# Printouts
process.MessageLogger = cms.Service("MessageLogger",
      debugModules = cms.untracked.vstring('bosonPtWeight','weightAnalyzer'),
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
process.bosonPtWeight = cms.EDProducer("BosonPtWeightProducer",
      GenTag = cms.untracked.InputTag("generator"),
      BosonPtBinEdges = cms.untracked.vdouble(
               0.,  1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.,  9.
            , 10., 11., 12., 13., 14., 15., 16., 17., 18., 19.
            , 20., 21., 22., 23., 24., 25., 26., 27., 28., 29.
            , 30., 31., 32., 33., 34., 35., 36., 37., 38., 39.
            , 40., 41., 42., 43., 44., 45., 46., 47., 48., 49.
            , 999999.
      ),
      PtWeights = cms.untracked.vdouble( 
              0.800665, 0.822121, 0.851249, 0.868285, 0.878733
            , 0.953853, 0.928108, 0.982021, 1.00659 , 1.00648
            , 1.03218 , 1.04924 , 1.03621 , 1.08743 , 1.01951
            , 1.10519 , 0.984263, 1.04853 , 1.06724 , 1.10183
            , 1.0503  , 1.13162 , 1.03837 , 1.12936 , 0.999173
            , 1.01453 , 1.11435 , 1.10545 , 1.07199 , 1.04542
            , 1.00828 , 1.0822  , 1.09667 , 1.16144 , 1.13906
            , 1.27974 , 1.14936 , 1.23235 , 1.06667 , 1.06363
            , 1.14225 , 1.22955 , 1.12674 , 1.03944 , 1.04639
            , 1.13667 , 1.20493 , 1.09349 , 1.2107  , 1.21073
      )
)

# Check that it is fine
process.weightAnalyzer = cms.EDFilter("BosonPtWeightAnalyzer",
      WeightTag = cms.untracked.InputTag("bosonPtWeight")
)

# Save weights in the output file 
process.load("Configuration.EventContent.EventContent_cff")
process.MyEventContent = cms.PSet( 
      outputCommands = process.AODSIMEventContent.outputCommands
)
process.MyEventContent.outputCommands.extend(
      cms.untracked.vstring('keep *_bosonPtWeight_*_*')
)

# Output (optionaly filtered by path)
process.output = cms.OutputModule("PoolOutputModule",
    process.MyEventContent,
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('bosonPtAna')
    ),
    fileName = cms.untracked.string('bosonPtWeighted_Events.root')
)

# Runnning and end paths
process.bosonPtAna = cms.Path(process.bosonPtWeight*process.weightAnalyzer)
process.end = cms.EndPath(process.output)
