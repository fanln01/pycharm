const { pdist, squareform } = require('scipy.spatial.distance');

function calculateAllDistances(nodes) {
    const pairwiseDistances = pdist(nodes);
    return squareform(pairwiseDistances);
}

const nodes = [
    [0.77175866, 0.37316362],
    [0.70169764, -0.03684474],
    [0.66292529, -0.28343777],
    // Add the rest of the node coordinates here...
];

const distancesMatrix = calculateAllDistances(nodes);
console.log(distancesMatrix);
