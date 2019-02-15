def plotdf(df, x, y, c=None, sample=10000, alpha=0.5, color=None,
           cmap='viridis', clabel=None, xlabel=None, ylabel=None,
           noise_df=None, percentile=0.98, use_noise_df_for_framing=False,
          noise_alpha=0.1):
    
    cols_to_get = [x, y]
    if c is not None:
        cols_to_get.append(c)
    
    df = df[cols_to_get]
    
    if noise_df is not None:
        if sample is not None:
            noise_df = noise_df[cols_to_get].sample((int(noise_df.shape[0]/df.shape[0]*sample))).copy()
        else:
            noise_df = noise_df[cols_to_get].copy()
    
    if sample is not None:
        df = df.sample(sample).copy()
    
    kwargs = dict(
            kind='scatter',
            alpha=alpha)
    
    if sample is not None:
        kwargs = {**kwargs,
                  **dict(s=20*np.sqrt(1.0/sample))}
    else:
        kwargs = {**kwargs,
                  **dict(s=20*np.sqrt(1.0/len(df[x])))}
    
    if c is not None:
        kwargs = {**kwargs,
                  **dict(c=c,
                        cmap=cmap,
                       vmin=df[c].quantile(0.01),
                       vmax=df[c].quantile(0.99))}
        
    elif color is not None:
        kwargs = {**kwargs,
                  **dict(color=color)}
        
        
    df.plot(x, y, **kwargs, zorder=2)
    
        
    
    if noise_df is not None:
        
        noise_df.plot(x, y, color='gray', kind='scatter', ax=plt.gcf().get_axes()[0], s=kwargs['s'], alpha=noise_alpha, zorder=1)

    top_percentile = 1 - (1-percentile)/2
    bottom_percentile = (1-percentile)/2
        
    if not use_noise_df_for_framing:
        plt.ylim(df[y].quantile(bottom_percentile), df[y].quantile(top_percentile))
        plt.xlim(df[x].quantile(bottom_percentile), df[x].quantile(top_percentile))
    else:
        #Assumes noise_df is bigger!
        plt.ylim(noise_df[y].quantile(bottom_percentile), noise_df[y].quantile(top_percentile))
        plt.xlim(noise_df[x].quantile(bottom_percentile), noise_df[x].quantile(top_percentile))
    
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if clabel is not None:
        f = plt.gcf()
        cax = f.get_axes()[1]
        cax.set_ylabel(clabel)
        
        
    return plt.gcf()
