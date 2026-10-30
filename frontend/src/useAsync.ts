import { useCallback, useEffect, useState } from 'react';

interface AsyncState<T> {
  data: T | undefined;
  error: string | undefined;
  loading: boolean;
}

export function useAsync<T>(load: () => Promise<T>, deps: unknown[]) {
  const [state, setState] = useState<AsyncState<T>>({ data: undefined, error: undefined, loading: true });
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let active = true;
    setState((previous) => ({ ...previous, loading: true, error: undefined }));
    load()
      .then((data) => active && setState({ data, error: undefined, loading: false }))
      .catch((error: unknown) =>
        active &&
        setState((previous) => ({
          ...previous,
          error: error instanceof Error ? error.message : 'Something went wrong.',
          loading: false,
        })),
      );
    return () => {
      active = false;
    };
  }, [version, ...deps]);

  const reload = useCallback(() => setVersion((value) => value + 1), []);

  return { ...state, reload };
}
