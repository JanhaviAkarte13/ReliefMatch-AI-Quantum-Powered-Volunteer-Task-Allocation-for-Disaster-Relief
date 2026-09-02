// Will chart quantum (QAOA) vs classical (Hungarian algorithm) results —
// fit score, tasks covered, solve time — using recharts. Built after
// AssignmentResults.jsx is wired up; left as a stub for now.
export default function ComparisonChart() {
  return (
    <div className="panel" style={{ textAlign: 'center', padding: '48px 24px' }}>
      <p style={{ color: 'var(--text-muted)', fontSize: 13.5, margin: 0 }}>
        Built after "Generate Assignment" is wired up — run an assignment first,
        then this chart will compare the quantum (QAOA) result against the
        classical (Hungarian algorithm) result.
      </p>
    </div>
  );
}
