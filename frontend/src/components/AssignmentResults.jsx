// Will render the volunteer-task assignment table returned by
// POST /assignments/generate (see apiClient.js). Built in the next step —
// left as a stub for now so Dashboard.jsx can already import and route to it.
export default function AssignmentResults() {
  return (
    <div className="panel" style={{ textAlign: 'center', padding: '48px 24px' }}>
      <p style={{ color: 'var(--text-muted)', fontSize: 13.5, margin: '0 0 16px' }}>
        Next build step — the "Generate Assignment" button and the resulting
        volunteer-task table will go here.
      </p>
      <button className="btn btn-primary" disabled>
        Generate Assignment
      </button>
    </div>
  );
}
