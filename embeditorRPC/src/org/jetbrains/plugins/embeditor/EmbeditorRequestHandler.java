package org.jetbrains.plugins.embeditor;

import com.intellij.codeInsight.completion.CompletionParameters;
import com.intellij.codeInsight.lookup.LookupElement;
import com.intellij.openapi.diagnostic.Logger;
import com.intellij.openapi.editor.Document;
import com.intellij.psi.PsiFile;
import com.intellij.util.ui.UIUtil;
import org.jetbrains.annotations.NotNull;

import java.util.Hashtable;
import java.util.List;

@SuppressWarnings("UnusedDeclaration")
public class EmbeditorRequestHandler {
    private final static Logger LOG = Logger.getInstance(EmbeditorRequestHandler.class);

    public Hashtable[] resolve(String path, String fileContent, int line, int column) {
        LOG.debug(String.format("resolve(%s:%d:%d)", path, line, column));
        List<ResolveOutcome> resolveOutcomes = EmbeditorUtil.getResolveOutcomes(path, fileContent, line, column);
        Hashtable[] results = new Hashtable[resolveOutcomes.size()];
        for (int i = 0; i < resolveOutcomes.size(); i++) {
            ResolveOutcome resolveOutcome = resolveOutcomes.get(i);
            Hashtable<String, Object> result = new Hashtable<String, Object>();
            result.put("path", resolveOutcome.getFilePath());
            result.put("line", resolveOutcome.getRow());
            result.put("column", resolveOutcome.getColumn());
            result.put("text", resolveOutcome.getText());
            results[i] = result;
        }
        return results;
    }

    public int getCompletionStartOffsetInLine(String path, String fileContent, int line, int column) {
        LOG.debug(String.format("getCompletionStartOffsetInLine(%s:%d:%d)", path, line, column));
        final int[] resultWrapper = new int[1];
        EmbeditorUtil.performCompletion(path, fileContent, line, column, new EmbeditorUtil.CompletionCallback() {
            @Override
            public void completionFinished(@NotNull CompletionParameters parameters,
                                           @NotNull LookupElement[] items,
                                           @NotNull Document document) {
                resultWrapper[0] = EmbeditorUtil.getOffsetFromLineStart(parameters, document);
            }
        });
        return resultWrapper[0];
    }

    public String[] getCompletionVariants(String path, String fileContent, int line, int column) {
        LOG.debug(String.format("getCompletionVariants(%s:%d:%d)", path, line, column));
        final String[][] resultsWrapper = new String[1][];
        EmbeditorUtil.performCompletion(path, fileContent, line, column, new EmbeditorUtil.CompletionCallback() {
            @Override
            public void completionFinished(@NotNull CompletionParameters parameters,
                                           @NotNull LookupElement[] items,
                                           @NotNull Document document) {
                String[] results = new String[items.length];
                for (int i = 0; i < items.length; i++) {
                    LookupElement item = items[i];
                    results[i] = item.getLookupString();
                }
                resultsWrapper[0] = results;
            }
        });
        return resultsWrapper[0];
    }

    public Hashtable[] inspectCode(final String path, String fileContent) {
        final Hashtable[][] resultsWrapper = new Hashtable[1][];
        UIUtil.invokeAndWaitIfNeeded(new Runnable() {
            @Override
            public void run() {
                PsiFile file = EmbeditorUtil.findTargetFile(path);
                if (file != null) {
                    List<Problem> problems = CodeInspector.inspect(file);
                    Hashtable[] results = new Hashtable[problems.size()];
                    for (int i = 0; i < problems.size(); i++) {
                        Problem problem = problems.get(i);
                        Hashtable<String, Object> result = new Hashtable<String, Object>();
                        result.put("line", problem.getLine());
                        result.put("column", problem.getColumn());
                        result.put("text", problem.getText());
                        results[i] = result;
                    }
                    resultsWrapper[0] = results;
                }
            }
        });
        return resultsWrapper[0];
    }
}
