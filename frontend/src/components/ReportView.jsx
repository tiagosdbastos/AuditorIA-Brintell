import React, { useRef } from "react";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import ReportCard from "./ReportCard";

export default function ReportView({ report, onNewAnalysis }) {
  const reportRef = useRef();

  const exportToPDF = async () => {
    const element = reportRef.current;
    const canvas = await html2canvas(element, { scale: 2 });
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");
    const width = pdf.internal.pageSize.getWidth();
    const height = (canvas.height * width) / canvas.width;
    pdf.addImage(imgData, "PNG", 0, 0, width, height);
    pdf.save("relatorio_auditorIA.pdf");
  };

  return (
    <section className="report-view">
      <h2>📋 Relatório de Análise</h2>

      <div className="report-content" ref={reportRef}>
        <div className="report-columns">
          <ReportCard title="Resumo do Edital">
            <p><strong>Objeto:</strong> {report.resumo.objeto}</p>
            <p><strong>Modalidade:</strong> {report.resumo.modalidade}</p>
            <p><strong>Valor Estimado:</strong> {report.resumo.valor}</p>
          </ReportCard>

          <ReportCard title="Cláusulas de Risco">
            <ul>{report.riscos.map((r, i) => <li key={i}>{r}</li>)}</ul>
          </ReportCard>

          <ReportCard title="Legislação Aplicável">
            <ul>{report.legislacao.map((l, i) => <li key={i}>{l}</li>)}</ul>
          </ReportCard>

          <ReportCard title="Jurisprudência Relevante">
            <ul>{report.jurisprudencia.map((j, i) => <li key={i}>{j}</li>)}</ul>
          </ReportCard>

          <ReportCard title="Conclusão" className="conclusion">
            <p>{report.conclusao}</p>
          </ReportCard>
        </div>
      </div>

      <div className="controls">
        <button className="btn pdf" onClick={exportToPDF}>
          📄 Exportar PDF
        </button>
        <button className="btn secondary" onClick={onNewAnalysis}>
          🔁 Nova Análise
        </button>
      </div>
    </section>
  );
}
