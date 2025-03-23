import React from 'react';
import { ReactFlowProvider } from 'reactflow';
import FamilyTreeGraphContent from './components/FamilyTreeGraphContent';
// ...existing code...

function App() {
  return (
    <ReactFlowProvider>
      {/* ...existing code... */}
      <FamilyTreeGraphContent />
      {/* ...existing code... */}
    </ReactFlowProvider>
  );
}

export default App;
