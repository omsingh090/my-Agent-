import { statusLabel, statusTone } from "@/lib/status";
import type { EvidenceStatus } from "@/types/portfolio";

export function StatusBadge({ status }: { status: EvidenceStatus }) {
  return (
    <span className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${statusTone(status)}`}>
      {statusLabel(status)}
    </span>
  );
}
