import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import { useRef } from "react";
import ReactMarkdown from "react-markdown";

export default function ReportView({ report, onNewAnalysis }) {
  const reportRef = useRef();

  const exportToPDF = async () => {
    const element = reportRef.current;

    // 1. Força o navegador a rolar para o topo para evitar falhas na captura
    window.scrollTo(0, 0);

    // 2. Captura o elemento inteiro (incluindo o que não cabe na tela)
    const canvas = await html2canvas(element, {
      scale: 2, // Mantém a alta qualidade
      useCORS: true,
      // Estas 3 linhas são o segredo para não cortar:
      height: element.scrollHeight, // Define a altura da captura como a altura TOTAL do conteúdo
      windowHeight: element.scrollHeight, // Simula uma janela gigante para caber tudo
      scrollY: 0 // Ignora a rolagem atual do usuário
    });

    const imgData = canvas.toDataURL("image/png");

    // 3. Calcula o tamanho do PDF baseado na imagem gerada
    const imgWidth = canvas.width;
    const imgHeight = canvas.height;

    // Converte pixels para milímetros (aprox. 1px = 0.26mm)
    const pdfWidth = imgWidth * 0.2645833333;
    const pdfHeight = imgHeight * 0.2645833333;

    // 4. Cria um PDF com o tamanho exato do conteúdo (Página Longa)
    // Assim não há quebras de página nem cortes no meio do texto
    const pdf = new jsPDF('p', 'mm', [pdfWidth, pdfHeight]);

    pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
    pdf.save("relatorio_auditorIA.pdf");
  };

  return (
    <section className="report-view">
      <h2>📋 Relatório de Análise</h2>

      <div className="report-content" ref={reportRef}>
        {/* Aqui mantemos o SEU layout original ou o Markdown, conforme preferir */}
        <div className="report-columns">
           <ReactMarkdown>
              {report.relatorio_final}
           </ReactMarkdown>
        </div>
      </div>

      <div className="controls">
        <button className="btn pdf" onClick={exportToPDF}>
          📄 Baixar PDF
        </button>
        <button className="btn secondary" onClick={onNewAnalysis}>
          🔁 Nova Análise
        </button>
      </div>
    </section>
  );
}
