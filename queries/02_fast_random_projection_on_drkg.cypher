CALL gds.fastRP.write("drkg-undirected",
{
    embeddingDimension: 512,
    iterationWeights: [0.2, 0.2, 0.75, 6.34, 0.7],
    writeProperty: 'embeddingVectorFastRP',
    normalizationStrength: -0.04,
    concurrency: 4
})
